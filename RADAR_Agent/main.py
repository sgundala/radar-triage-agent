"""MAIN — assemble the six blocks into one Agent, then run.

Run it:  uv run main.py

Nothing here is new. Every piece was written in its own block file; this file
only puts them together and feeds turns in.

    Agent(...)  IS Block 2 (state) + Block 3's assembling + the agentic loop.

THE TWO LOOPS — say this clearly when you teach it
Once this runs there are two loops, and confusing them is the classic mistake.

    YOUR OUTER LOOP      the while below. It does one thing: collect an
                         analyst message and print a reply. A chat box.

    STRANDS' INNER LOOP  hidden inside the single call agent(user_msg). The
                         model reads the conversation, requests a tool, the
                         SDK runs it and appends the result to the messages,
                         the model reads that and reasons again — possibly
                         several times — before that ONE line returns.

Yesterday you hand-wrote the inner loop. Today it is one function call.

And notice what is NOT in this file: nowhere do we write "first call
get_risk_evaluation, then get_risk_signals, then draft a rule." There is no
if/else choosing tools. The MODEL sequences them at run time from the
docstrings and the goal. That is what model-driven means.
"""

from strands import Agent

from block1_system_prompt import SYSTEM_PROMPT      # BLOCK 1 · you wrote it
from block3_input import READ_TOOLS                 # BLOCK 3 · your read tools
from block4_output import DRAFT_TOOLS               # BLOCK 4 · your draft tool
from block5_inference import model                  # BLOCK 5 · you wrote it
# BLOCK 2 (state) and the message assembling half of BLOCK 3: Strands, below.
# BLOCK 6 (eval logging) runs inside each tool — see block6_eval.py.

agent = Agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=READ_TOOLS + DRAFT_TOOLS,   # the hands we chose: three read, one draft
)


def run_triage() -> None:
    """Feed analyst turns to the agent until they quit."""
    print("Radar triage assistant. Try:  what's in my review queue?")
    print("(type quit to exit)\n")

    while True:
        user_msg = input("Analyst: ").strip()

        if user_msg.lower() in {"quit", "exit"}:
            print("Ending session. tool_calls.jsonl has the trace.")
            return

        if not user_msg:
            continue

        # One line of ours. A whole agentic loop of theirs.
        result = agent(user_msg)

        print(f"\nAssistant: {result}\n")


if __name__ == "__main__":     # runs only when executed directly
    run_triage()
