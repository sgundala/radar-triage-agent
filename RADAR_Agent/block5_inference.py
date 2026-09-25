"""BLOCK 5 · INFERENCE CONFIG  —  YOU BUILD THIS. The last block we write.

Who owns this block today:  YOU.

Strands is an AWS SDK, so out of the box it points at Amazon Bedrock and needs
AWS credentials nobody in this room has. If you skip this file you get a
Bedrock or AWS-credentials error on the very first run — that is the single
most common first-run failure today.

The fix is one object. Strands is MODEL-AGNOSTIC: it does not care who serves
the model. We route it through LiteLLM to OpenRouter and keep using the same
key from yesterday.

    Strands  ->  LiteLLM  ->  OpenRouter  ->  Claude

One arrow you can re-point. Provider choice is config, not architecture.

The dials are the same three as yesterday, chosen for the same reasons:

    model_id     one string swaps the entire engine
    temperature  0.2 — fraud triage wants steady and repeatable, not creative
    max_tokens   700 — an explanation plus a drafted rule, and a cost cap
"""

import os

from dotenv import load_dotenv
from strands.models.litellm import LiteLLMModel

load_dotenv()   # read .env into the environment

# ══════════════════════════════════════════════════════════════════════════
# OPTIONAL · LOCAL LLM VIA OLLAMA  (off by default — nothing below changes
# unless you flip the switch in .env)
#
#     USE_LOCAL_LLM=1                       flip the switch
#     LOCAL_MODEL=qwen2.5:7b                any model you have pulled (optional)
#     OLLAMA_BASE_URL=http://localhost:11434 where Ollama listens (optional)
#
# Why it exists: no API key, no credits, no network. Useful when OpenRouter
# says 402 or when you are offline. Same LiteLLM adapter, same Agent, same
# tools — only the arrow is re-pointed:
#
#     Strands  ->  LiteLLM  ->  Ollama (your machine)  ->  qwen / llama
#
# Pick a model that supports tool calling (qwen2.5, llama3.1, hermes3 do).
# Check what you have with:  ollama list        Pull one with:  ollama pull qwen2.5:7b
# ══════════════════════════════════════════════════════════════════════════
USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "").strip().lower() in {"1", "true", "yes"}

if USE_LOCAL_LLM:
    _local_model = os.getenv("LOCAL_MODEL", "qwen2.5:7b")
    _ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    model = LiteLLMModel(
        client_args={"api_base": _ollama_url},          # no api_key needed locally
        model_id=f"ollama_chat/{_local_model}",          # "ollama_chat/" = LiteLLM's Ollama chat route
        # max_tokens is HIGHER here on purpose. Small local models narrate
        # ("Step 1: let's list the payments...") before they call a tool. At
        # 700 the tool-call JSON gets cut off mid-write, Strands raises
        # MaxTokensReachedException, and the turn dies. 2000 leaves room.
        params={"temperature": 0.2, "max_tokens": 2000},
    )
    print(f"[inference] LOCAL model via Ollama: {_local_model} @ {_ollama_url}")

else:
    # ── DEFAULT · OPENROUTER (the original path, unchanged) ─────────────
    _api_key = os.getenv("OPENROUTER_API_KEY")
    if not _api_key:
        raise SystemExit(
            "No OPENROUTER_API_KEY found.\n"
            "  1. copy .env.example to .env\n"
            "  2. paste your key after OPENROUTER_API_KEY=\n"
            "  3. run again with:  uv run main.py"
        )

    model = LiteLLMModel(
        client_args={"api_key": _api_key},                  # never hard-coded
        model_id="openrouter/anthropic/claude-sonnet-4.6",  # provider/vendor/model
        params={"temperature": 0.2, "max_tokens": 700},
    )


# ── Convention nobody explains ───────────────────────────────────────────
# The model id is a PATH, not a name: "openrouter/anthropic/claude-sonnet-4.6".
# The first segment tells LiteLLM which provider to route to; the rest is that
# provider's own name for the model. Same Claude as yesterday — only the
# addressing changed, because we are reaching it through a different SDK.
