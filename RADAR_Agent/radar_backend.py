"""NOT A BLOCK — the simulated Stripe Radar backend.

In production these payments come from a live Stripe account. We do not wire
one up in class, so this file stands in for it: 30 payments across the whole
risk spectrum, each one a different fraud pattern.

Everything about the SHAPE here is from Stripe's published documentation:

    risk_score   0 (least risky) to 100 (riskiest)
    risk_level   normal / elevated / highest

Radar auto-blocks 'highest'. 'normal' clears. Only 'elevated' reaches a human
review queue — which is exactly the set our agent is allowed to look at.

    13 elevated   the review queue. These are what the agent investigates.
     5 highest    auto-blocked. Here only to prove they never reach the queue.
    12 normal     cleared. Same reason.

WHY SO MANY: so the agent is worth talking to. Every elevated payment tells a
different story, so two students investigating two payments get two genuinely
different conversations — not the same demo twice.

SIGNALS: every payment carries the same six core signals, plus extras that
matter for its particular pattern. That is realistic — real fraud data is
uneven, and an agent has to reason over what it actually gets back.

Keep this file boring. It is data, not a lesson.
"""

PAYMENTS = {

    # ══════════════════════════════════════════════════════════════════
    # ELEVATED — the review queue. A human decides on every one of these.
    # ══════════════════════════════════════════════════════════════════

    # ── The classic. Start here in class; it is the clearest story. ────
    "pay_card_testing": {
        "amount_usd": 4.99,
        "card_country": "US",
        "ip_country": "NG",
        "risk_score": 88,
        "risk_level": "elevated",
        "signals": {
            "attempts_from_ip_5min": 14,
            "cvc_check": "fail",
            "avs_check": "unavailable",
            "card_funding": "prepaid",
            "email_domain": "disposable",
            "proxy_or_vpn": True,
            "distinct_cards_this_ip_24h": 31,
        },
    },

    # ── The false positive. Demo this SECOND. A real customer. ─────────
    "pay_traveller": {
        "amount_usd": 890.00,
        "card_country": "US",
        "ip_country": "ES",
        "risk_score": 61,
        "risk_level": "elevated",
        "signals": {
            "attempts_from_ip_5min": 1,
            "cvc_check": "pass",
            "avs_check": "pass",
            "card_funding": "credit",
            "email_domain": "established",
            "proxy_or_vpn": False,
            "customer_account_age_days": 1120,
            "prior_successful_payments": 47,
        },
    },

    # ── Account takeover: the account is old, the behaviour is new. ────
    "pay_account_takeover": {
        "amount_usd": 1450.00,
        "card_country": "US",
        "ip_country": "US",
        "risk_score": 79,
        "risk_level": "elevated",
        "signals": {
            "attempts_from_ip_5min": 2,
            "cvc_check": "pass",
            "avs_check": "pass",
            "card_funding": "credit",
            "email_domain": "established",
            "proxy_or_vpn": False,
            "customer_account_age_days": 830,
            "shipping_address_changed_hours_ago": 2,
            "device_new": True,
            "password_changed_hours_ago": 3,
        },
    },

    # ── BIN attack: sequential card numbers, one IP block. ─────────────
    "pay_bin_attack": {
        "amount_usd": 1.00,
        "card_country": "US",
        "ip_country": "VN",
        "risk_score": 91,
        "risk_level": "elevated",
        "signals": {
            "attempts_from_ip_5min": 22,
            "cvc_check": "fail",
            "avs_check": "fail",
            "card_funding": "credit",
            "email_domain": "disposable",
            "proxy_or_vpn": True,
            "sequential_card_numbers": True,
            "distinct_cards_this_ip_24h": 88,
        },
    },

    # ── Reshipper / freight forwarder as the shipping address. ─────────
    "pay_reshipper": {
        "amount_usd": 2300.00,
        "card_country": "US",
        "ip_country": "US",
        "risk_score": 74,
        "risk_level": "elevated",
        "signals": {
            "attempts_from_ip_5min": 1,
            "cvc_check": "pass",
            "avs_check": "pass",
            "card_funding": "credit",
            "email_domain": "new",
            "proxy_or_vpn": False,
            "shipping_billing_match": False,
            "shipping_is_freight_forwarder": True,
            "customer_account_age_days": 4,
        },
    },

    # ── Gift-card reseller: digital goods, many cards, one email. ──────
    "pay_giftcard_bulk": {
        "amount_usd": 500.00,
        "card_country": "GB",
        "ip_country": "GB",
        "risk_score": 83,
        "risk_level": "elevated",
        "signals": {
            "attempts_from_ip_5min": 6,
            "cvc_check": "pass",
            "avs_check": "unavailable",
            "card_funding": "prepaid",
            "email_domain": "established",
            "proxy_or_vpn": False,
            "distinct_cards_this_email_24h": 9,
            "merchant_category": "digital_giftcards",
        },
    },

    # ── Genuinely ambiguous: big first purchase, everything checks out. ─
    "pay_first_time_big": {
        "amount_usd": 3200.00,
        "card_country": "US",
        "ip_country": "US",
        "risk_score": 66,
        "risk_level": "elevated",
        "signals": {
            "attempts_from_ip_5min": 1,
            "cvc_check": "pass",
            "avs_check": "pass",
            "card_funding": "credit",
            "email_domain": "established",
            "proxy_or_vpn": False,
            "customer_account_age_days": 0,
            "prior_successful_payments": 0,
            "three_ds_result": "authenticated",
        },
    },

    # ── Free-trial abuse: same device fingerprint, many signups. ───────
    "pay_trial_abuse": {
        "amount_usd": 0.50,
        "card_country": "US",
        "ip_country": "US",
        "risk_score": 71,
        "risk_level": "elevated",
        "signals": {
            "attempts_from_ip_5min": 4,
            "cvc_check": "pass",
            "avs_check": "pass",
            "card_funding": "debit",
            "email_domain": "new",
            "proxy_or_vpn": False,
            "same_device_signups_7d": 17,
            "merchant_category": "subscription_trial",
        },
    },

    # ── VPN, but a plausible one. The privacy-conscious customer. ──────
    "pay_vpn_legit": {
        "amount_usd": 129.00,
        "card_country": "DE",
        "ip_country": "CH",
        "risk_score": 58,
        "risk_level": "elevated",
        "signals": {
            "attempts_from_ip_5min": 1,
            "cvc_check": "pass",
            "avs_check": "unavailable",
            "card_funding": "credit",
            "email_domain": "established",
            "proxy_or_vpn": True,
            "customer_account_age_days": 612,
            "prior_successful_payments": 23,
        },
    },

    # ── Prior chargebacks: the customer is real and the risk is real. ──
    "pay_chargeback_history": {
        "amount_usd": 640.00,
        "card_country": "US",
        "ip_country": "US",
        "risk_score": 77,
        "risk_level": "elevated",
        "signals": {
            "attempts_from_ip_5min": 1,
            "cvc_check": "pass",
            "avs_check": "pass",
            "card_funding": "credit",
            "email_domain": "established",
            "proxy_or_vpn": False,
            "customer_account_age_days": 390,
            "prior_chargebacks": 3,
            "prior_successful_payments": 11,
        },
    },

    # ── Velocity, but a legitimate business buying in bulk. ────────────
    "pay_bulk_legit": {
        "amount_usd": 75.00,
        "card_country": "CA",
        "ip_country": "CA",
        "risk_score": 55,
        "risk_level": "elevated",
        "signals": {
            "attempts_from_ip_5min": 9,
            "cvc_check": "pass",
            "avs_check": "pass",
            "card_funding": "credit",
            "email_domain": "corporate",
            "proxy_or_vpn": False,
            "customer_account_age_days": 2200,
            "prior_successful_payments": 310,
            "merchant_category": "office_supplies",
        },
    },

    # ── Refund abuse: buys, refunds, repeats. ─────────────────────────
    "pay_refund_abuse": {
        "amount_usd": 215.00,
        "card_country": "AU",
        "ip_country": "AU",
        "risk_score": 69,
        "risk_level": "elevated",
        "signals": {
            "attempts_from_ip_5min": 1,
            "cvc_check": "pass",
            "avs_check": "pass",
            "card_funding": "debit",
            "email_domain": "established",
            "proxy_or_vpn": False,
            "customer_account_age_days": 180,
            "refund_rate_90d": 0.82,
            "prior_successful_payments": 17,
        },
    },

    # ── Odd hour, corporate card. Weak signal on its own. ─────────────
    "pay_odd_hours": {
        "amount_usd": 1180.00,
        "card_country": "US",
        "ip_country": "US",
        "risk_score": 52,
        "risk_level": "elevated",
        "signals": {
            "attempts_from_ip_5min": 1,
            "cvc_check": "pass",
            "avs_check": "pass",
            "card_funding": "credit",
            "email_domain": "corporate",
            "proxy_or_vpn": False,
            "customer_account_age_days": 95,
            "hour_local": 3,
            "distinct_ips_this_card_24h": 4,
        },
    },

    # ══════════════════════════════════════════════════════════════════
    # HIGHEST — auto-blocked by Radar's own model. Never reaches a human.
    # Here so list_flagged_payments can prove it filters them out.
    # ══════════════════════════════════════════════════════════════════

    "pay_stolen_card": {
        "amount_usd": 1899.00, "card_country": "US", "ip_country": "RU",
        "risk_score": 97, "risk_level": "highest",
        "signals": {"attempts_from_ip_5min": 3, "cvc_check": "fail",
                    "avs_check": "fail", "card_funding": "credit",
                    "email_domain": "disposable", "proxy_or_vpn": True,
                    "card_reported_stolen": True},
    },
    "pay_extreme_velocity": {
        "amount_usd": 2.00, "card_country": "BR", "ip_country": "BR",
        "risk_score": 99, "risk_level": "highest",
        "signals": {"attempts_from_ip_5min": 140, "cvc_check": "fail",
                    "avs_check": "unavailable", "card_funding": "prepaid",
                    "email_domain": "disposable", "proxy_or_vpn": True,
                    "distinct_cards_this_ip_24h": 410},
    },
    "pay_blocklist_email": {
        "amount_usd": 340.00, "card_country": "US", "ip_country": "US",
        "risk_score": 94, "risk_level": "highest",
        "signals": {"attempts_from_ip_5min": 2, "cvc_check": "pass",
                    "avs_check": "fail", "card_funding": "prepaid",
                    "email_domain": "blocklisted", "proxy_or_vpn": True},
    },
    "pay_3ds_failures": {
        "amount_usd": 760.00, "card_country": "FR", "ip_country": "UA",
        "risk_score": 95, "risk_level": "highest",
        "signals": {"attempts_from_ip_5min": 8, "cvc_check": "fail",
                    "avs_check": "fail", "card_funding": "credit",
                    "email_domain": "new", "proxy_or_vpn": True,
                    "three_ds_result": "failed", "three_ds_attempts": 6},
    },
    "pay_known_fraud_ring": {
        "amount_usd": 4500.00, "card_country": "US", "ip_country": "US",
        "risk_score": 96, "risk_level": "highest",
        "signals": {"attempts_from_ip_5min": 1, "cvc_check": "pass",
                    "avs_check": "pass", "card_funding": "credit",
                    "email_domain": "new", "proxy_or_vpn": False,
                    "device_linked_to_confirmed_fraud": True},
    },

    # ══════════════════════════════════════════════════════════════════
    # NORMAL — cleared automatically. Never reaches a human either.
    # ══════════════════════════════════════════════════════════════════

    "pay_normal_coffee": {
        "amount_usd": 6.40, "card_country": "US", "ip_country": "US",
        "risk_score": 3, "risk_level": "normal",
        "signals": {"attempts_from_ip_5min": 1, "cvc_check": "pass",
                    "avs_check": "pass", "card_funding": "credit",
                    "email_domain": "established", "proxy_or_vpn": False},
    },
    "pay_normal_subscription": {
        "amount_usd": 14.99, "card_country": "US", "ip_country": "US",
        "risk_score": 2, "risk_level": "normal",
        "signals": {"attempts_from_ip_5min": 1, "cvc_check": "pass",
                    "avs_check": "pass", "card_funding": "credit",
                    "email_domain": "established", "proxy_or_vpn": False,
                    "customer_account_age_days": 1400},
    },
    "pay_normal_groceries": {
        "amount_usd": 87.25, "card_country": "GB", "ip_country": "GB",
        "risk_score": 6, "risk_level": "normal",
        "signals": {"attempts_from_ip_5min": 1, "cvc_check": "pass",
                    "avs_check": "pass", "card_funding": "debit",
                    "email_domain": "established", "proxy_or_vpn": False},
    },
    "pay_normal_repeat": {
        "amount_usd": 42.00, "card_country": "US", "ip_country": "US",
        "risk_score": 4, "risk_level": "normal",
        "signals": {"attempts_from_ip_5min": 1, "cvc_check": "pass",
                    "avs_check": "pass", "card_funding": "credit",
                    "email_domain": "established", "proxy_or_vpn": False,
                    "prior_successful_payments": 96},
    },
    "pay_normal_books": {
        "amount_usd": 23.80, "card_country": "CA", "ip_country": "CA",
        "risk_score": 8, "risk_level": "normal",
        "signals": {"attempts_from_ip_5min": 1, "cvc_check": "pass",
                    "avs_check": "pass", "card_funding": "credit",
                    "email_domain": "established", "proxy_or_vpn": False},
    },
    "pay_normal_saas": {
        "amount_usd": 199.00, "card_country": "US", "ip_country": "US",
        "risk_score": 11, "risk_level": "normal",
        "signals": {"attempts_from_ip_5min": 1, "cvc_check": "pass",
                    "avs_check": "pass", "card_funding": "credit",
                    "email_domain": "corporate", "proxy_or_vpn": False,
                    "customer_account_age_days": 700},
    },
    "pay_normal_rideshare": {
        "amount_usd": 18.40, "card_country": "US", "ip_country": "US",
        "risk_score": 5, "risk_level": "normal",
        "signals": {"attempts_from_ip_5min": 1, "cvc_check": "pass",
                    "avs_check": "unavailable", "card_funding": "debit",
                    "email_domain": "established", "proxy_or_vpn": False},
    },
    "pay_normal_pharmacy": {
        "amount_usd": 31.15, "card_country": "US", "ip_country": "US",
        "risk_score": 7, "risk_level": "normal",
        "signals": {"attempts_from_ip_5min": 1, "cvc_check": "pass",
                    "avs_check": "pass", "card_funding": "debit",
                    "email_domain": "established", "proxy_or_vpn": False},
    },
    "pay_normal_hotel": {
        "amount_usd": 412.00, "card_country": "DE", "ip_country": "DE",
        "risk_score": 14, "risk_level": "normal",
        "signals": {"attempts_from_ip_5min": 1, "cvc_check": "pass",
                    "avs_check": "pass", "card_funding": "credit",
                    "email_domain": "established", "proxy_or_vpn": False,
                    "customer_account_age_days": 950},
    },
    "pay_normal_donation": {
        "amount_usd": 50.00, "card_country": "US", "ip_country": "US",
        "risk_score": 9, "risk_level": "normal",
        "signals": {"attempts_from_ip_5min": 1, "cvc_check": "pass",
                    "avs_check": "pass", "card_funding": "credit",
                    "email_domain": "established", "proxy_or_vpn": False},
    },
    "pay_normal_hardware": {
        "amount_usd": 156.70, "card_country": "US", "ip_country": "US",
        "risk_score": 12, "risk_level": "normal",
        "signals": {"attempts_from_ip_5min": 2, "cvc_check": "pass",
                    "avs_check": "pass", "card_funding": "credit",
                    "email_domain": "established", "proxy_or_vpn": False},
    },
    "pay_normal_flight": {
        "amount_usd": 680.00, "card_country": "US", "ip_country": "US",
        "risk_score": 16, "risk_level": "normal",
        "signals": {"attempts_from_ip_5min": 1, "cvc_check": "pass",
                    "avs_check": "pass", "card_funding": "credit",
                    "email_domain": "established", "proxy_or_vpn": False,
                    "three_ds_result": "authenticated"},
    },
}


# ══════════════════════════════════════════════════════════════════════
# TEACHING PICKS — which payment to reach for, and what it demonstrates
# ══════════════════════════════════════════════════════════════════════
#
#   pay_card_testing        open with this. The clearest story in the file.
#   pay_traveller           then this. A real customer who looks guilty.
#                           Does the drafted rule name its false positives?
#   pay_first_time_big      the hardest one. Every check passes, the account
#                           is zero days old, $3,200. There is no right
#                           answer — which is exactly the point.
#   pay_bulk_legit          velocity, but a 6-year corporate customer with
#                           310 prior payments. Kills "high velocity = fraud".
#   pay_account_takeover    old account, new device, address changed 2 hours
#                           ago. The fraud is the CHANGE, not any one value.
#   pay_vpn_legit           a VPN on a 612-day account. Weak signals stack
#                           badly when you rule on them alone.
#   pay_stolen_card         ask for it by name. It is 'highest' — auto-blocked
#                           and never in the queue. Proves the filter is real.
#
# Ask two students to investigate two different payments. They get genuinely
# different conversations, and comparing the two drafted rules is the best
# discussion in the session.
