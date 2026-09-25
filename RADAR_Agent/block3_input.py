"""BLOCK 3 · INPUT  —  SPLIT: Strands assembles it, YOU choose what can reach it.

Who owns this block today:  STRANDS for the assembling, YOU for the tools.

Yesterday you wrote build_messages() by hand: copy the history, append the new
message, inject a nudge. Today Strands does all of that inside agent(user_msg).

But something new decides what INFORMATION can get into those messages, and
that part is yours: the READ TOOLS below.

    A tool that fetches data is input engineering.

The model is text in, text out. It has never seen our payment data. So when
the analyst asks "why was this flagged?", the numbers have to come from
somewhere real — or the model invents them. These three tools are that
somewhere. The model requests one, Strands runs it, and the return value is
appended to the messages as a new entry, which the model reads on its next
pass. That is the bridge from "tool" to "the agentic loop".

WHY THE DOCSTRINGS MATTER MORE THAN THE CODE
Under each def below is a triple-quoted docstring. For a tool that is not
decoration — the model reads it to decide when to call the tool and with what
arguments. A vague docstring is a misused tool. For tools, the docstring IS
the interface.

That is also why "what's in my queue?", "anything to review?" and "show me
flagged payments" all reach the same tool: the model is matching the MEANING
of the question to the meaning of the docstring. Week 1, Day 2 — near
synonyms sit near each other in embedding space. Same idea, doing real work.
"""

from strands import tool

from block6_eval import log_tool_call
from radar_backend import PAYMENTS


@tool
def list_flagged_payments() -> list:
    """List the payments sitting in the review queue and their risk scores.

    Use this when the analyst asks what needs review, what is in the queue,
    or what has been flagged — without naming a specific payment.

    Only 'elevated' payments appear here: Stripe auto-blocks 'highest' and
    lets 'normal' through, so neither ever reaches a human.
    """
    result = sorted(
        (
            {"payment_id": pid, "risk_score": p["risk_score"]}
            for pid, p in PAYMENTS.items()
            if p["risk_level"] == "elevated"
        ),
        key=lambda row: row["risk_score"],
        reverse=True,          # riskiest first — how an analyst actually triages
    )
    # A short summary on purpose, not the full record. Every tool result is
    # fed back and re-tokenised on the next turn — thirteen rows of two fields
    # is cheap; thirteen full records with every signal would flood the
    # context window on every single turn, and five hundred would break it.
    log_tool_call("list_flagged_payments", {}, result)
    return result


@tool
def get_risk_evaluation(payment_id: str) -> dict:
    """Return Radar's risk evaluation for one payment.

    Gives the risk_score (0-100), the risk_level (normal/elevated/highest),
    the amount, and the card and IP countries. Use this first when asked to
    investigate a specific payment_id.
    """
    p = PAYMENTS.get(payment_id)
    if not p:
        # Handle bad input, never crash. A tool that throws on a bad argument
        # breaks the whole agentic loop — the model gets no result to reason
        # over and the turn dies.
        result = {"error": f"unknown payment_id: {payment_id}"}
    else:
        result = {k: p[k] for k in
                  ("amount_usd", "card_country", "ip_country", "risk_score", "risk_level")}

    log_tool_call("get_risk_evaluation", {"payment_id": payment_id}, result)
    return result


@tool
def get_risk_signals(payment_id: str) -> dict:
    """Return the detailed fraud signals behind a payment's risk score.

    Includes velocity (attempts from the same IP in five minutes), the AVS and
    CVC check results, whether a proxy or VPN was used, the card funding type,
    and whether the email domain is disposable. Use this after
    get_risk_evaluation when you need to explain WHY a payment was flagged.
    """
    p = PAYMENTS.get(payment_id)
    result = p["signals"] if p else {"error": f"unknown payment_id: {payment_id}"}

    log_tool_call("get_risk_signals", {"payment_id": payment_id}, result)
    return result


# Every tool here READS. Not one of them changes anything. That is deliberate,
# and Block 4 is where we make the point properly.
READ_TOOLS = [list_flagged_payments, get_risk_evaluation, get_risk_signals]
