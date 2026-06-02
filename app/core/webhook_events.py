# =========================================================
# RAZORPAY WEBHOOK EVENT -> INTERNAL STATE
# =========================================================

RAZORPAY_EVENT_STATE_MAP = {

    # -----------------------------------
    # PAYMENT SUCCESS
    # -----------------------------------

    "payment.captured": "CAPTURED",

    # -----------------------------------
    # PAYMENT FAILURE
    # -----------------------------------

    "payment.failed": "FAILED",

    # -----------------------------------
    # REFUND EVENTS
    # -----------------------------------

    "refund.processed": "REFUNDED"
}


# =========================================================
# STRIPE WEBHOOK EVENT -> INTERNAL STATE
# =========================================================

STRIPE_EVENT_STATE_MAP = {

    # -----------------------------------
    # PAYMENT SUCCESS
    # -----------------------------------

    "payment_intent.succeeded": "CAPTURED",

    # -----------------------------------
    # PAYMENT FAILURE
    # -----------------------------------

    "payment_intent.payment_failed": "FAILED",

    # -----------------------------------
    # REFUND EVENTS
    # -----------------------------------

    "charge.refunded": "REFUNDED"
}