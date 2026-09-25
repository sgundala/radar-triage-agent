"""BLOCK 2 · STATE  —  STRANDS OWNS THIS BLOCK. There is no code to write.

Who owns this block today:  STRANDS.

This file is deliberately almost empty. Open it in class, read it, and close
it. The point of the file existing at all is that the block still exists — the
work did not disappear, somebody else is doing it.

──────────────────────────────────────────────────────────────────────────
WHAT YOU WROTE YESTERDAY                 WHAT HAPPENS TODAY
──────────────────────────────────────────────────────────────────────────
@dataclass                               agent = Agent(...)
class IntakeState:
    policyholder_name: str | None        the Agent instance holds the
    ...                                  running conversation itself
    history: list = field(...)
    def missing_required(self)           you never see it, never name it,
    def ready_to_handoff(self)           never append to it
──────────────────────────────────────────────────────────────────────────

Say the trade out loud, because it is the honest part:

    Hidden is not gone. The state is still there — Strands owns it. You
    traded fine-grained control for speed, knowingly. Yesterday you could
    see and shape every byte of it. Today you trust the SDK's version.

That trade is fine here. It would not be fine in a regulated system where you
must prove exactly what was retained and for how long — and that is the kind
of judgement call this course is training you to make.

One thing worth knowing even though you did not write it: Strands keeps the
conversation on the Agent object, so a SECOND Agent() is a second, separate
conversation. Two analysts, two Agents, no crosstalk — the same reason
yesterday's IntakeState had to be one-per-conversation.
"""

# Nothing to import. Nothing to define. Strands' Agent(...) in main.py IS
# this block. That is the whole lesson.
