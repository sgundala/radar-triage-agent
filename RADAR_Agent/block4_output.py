"""BLOCK 4 · OUTPUT  —  YOU BUILD THIS, Strands delivers it.

Who owns this block today:  YOU for the tool, STRANDS for returning the reply.

One reply, two readers — the same discipline as yesterday. The analyst reads a
paragraph explaining the flag. The drafted rule is the structured part, and it
comes out of a tool rather than out of parsed JSON.

    Yesterday: the model emitted JSON and we parsed it.
    Today:     the model calls a tool and the tool shapes the structure.

Both are "structured output". Tomorrow LangChain does it a third way, with a
typed schema the reply must validate against. Three routes to the same goal;
you will have built all three.

──────────────────────────────────────────────────────────────────────────
THE SAFETY POINT — this is the most important idea in the file
──────────────────────────────────────────────────────────────────────────
Count the tools in this whole project:

    list_flagged_payments   reads
    get_risk_evaluation     reads
    get_risk_signals        reads
    draft_radar_rule        drafts text

There is NO tool that blocks, allows, or applies anything.

The agent cannot take the dangerous action because we never gave it the hands
to do it. That is LEAST PRIVILEGE, and it is a far stronger guardrail than
the sentence in Block 1. A prompt asks the model not to. A missing tool means
it cannot, however it is asked, however the conversation is manipulated.

The safest guardrail is the dangerous tool you never hand over.
"""

from strands import tool

from block6_eval import log_tool_call

# Stripe's real Radar rule actions. Anything else is rejected outright.
VALID_ACTIONS = {"Block", "Review", "Request3DS", "Allow"}


@tool
def draft_radar_rule(condition: str, action: str) -> str:
    """DRAFT a candidate Radar rule for a human analyst to review.

    This only proposes rule text. It never applies, activates, or enforces
    anything — a human reads the draft and decides.

    Write the condition in Stripe's rule syntax using :attribute: names, for
    example ":card_funding: = 'prepaid' AND :card_velocity: > 10".

    The action must be exactly one of: Block, Review, Request3DS, Allow.
    """
    if action not in VALID_ACTIONS:
        result = f"invalid action {action!r} — must be one of {sorted(VALID_ACTIONS)}"
    else:
        # The [DRAFT] marker is not cosmetic. It travels with the text into
        # whatever the analyst pastes it into, so the rule can never be
        # mistaken for one that is live.
        result = f"[DRAFT — needs human review] {action} if {condition}"

    log_tool_call("draft_radar_rule", {"condition": condition, "action": action}, result)
    return result


DRAFT_TOOLS = [draft_radar_rule]


# ── What to watch for the instant it speaks ──────────────────────────────
#
# It will say something like "14 attempts from one IP in five minutes". That
# is a specific number, stated confidently. Before you trust it, ask: did a
# tool actually return that?
#
# A HALLUCINATED SIGNAL is a fraud reason no tool ever returned. It is worse
# than a wrong rule — a human reviews the rule, but nobody double-checks the
# explanation, so an invented signal quietly sends the analyst down the wrong
# path.
#
# That is why every tool in this project logs its result (Block 6). Next
# session we read that log and compute the hallucinated-signal rate: of all
# the signals the assistant cited, how many appear in a real tool output.
