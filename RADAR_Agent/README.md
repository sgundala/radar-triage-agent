# Radar Triage Agent — Week 2, Day 2

A Stripe Radar fraud-triage assistant, built with the **Strands** SDK, as **one file
per block**. It investigates a flagged payment, explains why it was flagged, and drafts
a candidate rule.

**It never blocks, allows, or applies anything.** Not because the prompt says so — because
we never gave it a tool that can.

---

## Nothing installed yet? Start here. Three steps, about five minutes.

You need **Python** and **uv**. You do not need to understand either one yet.

### 1 · Python

Check whether you already have it. Open a terminal and type:

```bash
python3 --version
```

A version number means you are done. "command not found" means install it from
**python.org/downloads** — take the big yellow button, and on Windows **tick
"Add python.exe to PATH"** on the first screen of the installer. That tick box is the
single most common reason Python "doesn't work" afterwards.

### 2 · uv

One line, pasted into a terminal:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Then close the terminal and open a new one** — the installer edits your PATH and the
old window has not noticed. Check it worked:

```bash
uv --version
```

### 3 · This project

Open this folder in VS Code (File → Open Folder), open the terminal inside VS Code with
**Ctrl + `** (Cmd + ` on Mac), and run:

```bash
uv sync                  # installs everything, exactly
cp .env.example .env     # then paste your OpenRouter key into .env
uv run main.py           # run the agent
```

On Windows, use `copy .env.example .env` for the middle line.

That is it. **No `python -m venv`, no activate command, no `pip install`, no
requirements.txt.** `uv sync` reads `pyproject.toml`, builds the environment and
installs the exact versions. `uv run` uses that environment automatically, so there is
nothing to remember and nothing to activate.

Get a key at **openrouter.ai → Keys**. One key reaches every model.

### Optional · run on a local model instead (no key, no credits, no network)

Block 5 has a second, switched-off path that routes through **Ollama** on your own
machine. Same Strands `Agent`, same tools, same LiteLLM adapter — only the arrow is
re-pointed:

```
Strands  ->  LiteLLM  ->  Ollama (localhost)  ->  qwen / llama
```

Use it when OpenRouter returns a **402 out-of-credits** error, when you are offline, or
just to see how a 7B model handles the same tools.

```bash
# once: install Ollama from ollama.com, then pull a tool-calling model
ollama pull qwen2.5:7b

# then either uncomment USE_LOCAL_LLM=1 in .env, or flip it for one run:
USE_LOCAL_LLM=1 uv run main.py
```

Two optional overrides, also read from `.env`:

| Variable | Default | Meaning |
|---|---|---|
| `LOCAL_MODEL` | `qwen2.5:7b` | Any model in `ollama list`. Must support tool calling (qwen2.5, llama3.1, hermes3 do) |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Where Ollama is listening |

The first line printed tells you which engine you are on:
`[inference] LOCAL model via Ollama: qwen2.5:7b @ http://localhost:11434`.

Expect it to be weaker than Claude — it may over-investigate, or invent rule syntax.
That gap *is* the lesson: model choice is a dial, and Block 5 is where you turn it.

---

## The six blocks — and who builds each one today

Yesterday you hand-wrote all six. Today an SDK builds some for you. **Every block still
exists** — the files for the ones Strands owns are there to be read, not written.

| File | Block | Who builds it | What it holds |
|---|---|---|---|
| `block1_system_prompt.py` | 1 · System prompt | **you** | Role, scope, the "recommend only" guardrail |
| `block2_state.py` | 2 · State | **Strands** | Nothing to write. Read it, understand the trade |
| `block3_input.py` | 3 · Input | **split** | Strands assembles messages; **you** write the read tools |
| `block4_output.py` | 4 · Output | **you** | The draft tool — and the missing block tool |
| `block5_inference.py` | 5 · Inference config | **you** | LiteLLM → OpenRouter, temp 0.2 — or Ollama locally with `USE_LOCAL_LLM=1` |
| `block6_eval.py` | 6 · Eval | **you** | Tool-call logging — next session's raw material |
| `main.py` | — | — | Assembles the Agent and feeds turns in |
| `radar_backend.py` | — | — | Not a block. The simulated Stripe data |

Build order in class: **prompt → tools → config → assemble → run.** Nothing runs until
the last arrow.

---

## The two loops

```
your outer loop  ─ while True: input("Analyst: ")
                   │
                   └─ agent(user_msg)  ──────────────┐
                                                     │  STRANDS' INNER LOOP
                        model reads the conversation │
                        model requests a tool        │
                        SDK runs it, appends result  │  may go round
                        model reads the result       │  several times
                        ... until a final answer     │
                                                     │
                   ┌─────────────────────────────────┘
                   └─ print the reply
```

One line of yours. A whole loop of theirs.

**Nowhere do we write the sequence of tool calls.** There is no if/else picking tools.
The model sequences them at run time, from the docstrings and the goal. That is
*model-driven* control flow, and it is the new idea of the day.

---

## Why the tool list is the real guardrail

```
list_flagged_payments   reads
get_risk_evaluation     reads
get_risk_signals        reads
draft_radar_rule        drafts text
```

No tool blocks. No tool applies. The agent cannot take the dangerous action because it
has no hands for it. That is **least privilege**, and it holds however the conversation
is phrased or manipulated — which a sentence in a prompt does not.

---

## Try to break it

1. Ask it to block `pay_card_testing`. Watch it refuse, then check: was that the prompt,
   or the missing tool?
2. Ask "wasn't there also a chargeback on that one?" Does it agree? Nothing in any tool
   result mentions a chargeback — if it cites one, that is a **hallucinated signal**.
3. Investigate `pay_traveller`. It is a real customer with a 1,120-day-old account
   travelling in Spain. Does the drafted rule name the false positives it would cause?
4. Ask the same thing three ways: "what's in my queue?", "anything to review?", "show me
   flagged payments". All three should hit the same tool.

Bring `tool_calls.jsonl` to the next session. Every legitimate signal the assistant could
cite is in that file — anything it said that is *not* in there is what we measure.

---

## First-run errors, decoded

| What you see | What it means |
|---|---|
| Bedrock / AWS credentials error | Block 5 was skipped. Strands fell back to its AWS default |
| `ModuleNotFoundError: strands` | Wrong environment. Use `uv run main.py`, not the VS Code play button |
| `No OPENROUTER_API_KEY found` | No `.env` yet — copy `.env.example` and paste your key |
| `402 ... exceed your available credits` / `in_flight_budget_exhausted` | OpenRouter account has no credits. Top up at openrouter.ai → Credits, or run locally with `USE_LOCAL_LLM=1` |
| `Connection refused` on `localhost:11434` | `USE_LOCAL_LLM=1` is set but Ollama is not running. Start it with `ollama serve` (or open the Ollama app) |
| Nothing happens at all | Missing `if __name__ == "__main__":` at the bottom of `main.py` |
| `uv: command not found` | Installed, but the terminal is old. Close it, open a new one |
