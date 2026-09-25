"""BLOCK 6 · EVAL  —  YOU BUILD THE LOGGING. The numbers come next session.

Who owns this block today:  YOU.

"It worked when I tried it" is not an evaluation. An eval runs the agent over
many known cases and computes numbers. You cannot measure what you did not
record — so the only part we build today is the recording.

Every tool call in this project writes one line here: which tool, what
arguments, what it returned. Next session we read that file and compute two
numbers.

    HALLUCINATED-SIGNAL RATE
        Of all the signals the assistant cited in its explanation, how many
        never appear in any tool result? This is the number that matters. A
        confident invented signal misleads the analyst who trusts it.

    GUARDRAIL-VIOLATION RATE
        How often did it try to block or apply instead of recommend? Target
        is zero — and we made that very hard by never giving it a block tool.

Why the log is the evidence: the assistant's claims are in the transcript, and
every legitimate signal it could cite is in this file. Anything in the first
that is not in the second is a hallucination. That is the whole measurement,
and it only works because we wrote this file today.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path("tool_calls.jsonl")

# Flip to False if the tool trace is too noisy while you teach. The file still
# gets written either way — this only controls the terminal.
SHOW_IN_TERMINAL = True


def log_tool_call(tool_name: str, args: dict, result) -> None:
    """Record one tool call, to the screen and to tool_calls.jsonl.

    JSONL — one JSON object per line — is the standard shape for this. It
    appends cheaply, survives a crash mid-run, and every data tool reads it.

    Args:
        tool_name: the function the model asked for.
        args: the arguments the model chose.
        result: whatever the tool returned.
    """
    record = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tool": tool_name,
        "args": args,
        "result": result,
    }

    if SHOW_IN_TERMINAL:
        shown = json.dumps(result, default=str)
        if len(shown) > 160:
            shown = shown[:157] + "..."
        print(f"  [tool] {tool_name}({_fmt(args)}) -> {shown}")

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, default=str) + "\n")


def _fmt(args: dict) -> str:
    """Render the arguments the way a Python call would look."""
    return ", ".join(f"{k}={v!r}" for k, v in args.items())
