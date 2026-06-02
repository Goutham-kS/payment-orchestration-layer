# app/core/state_machine.py

# =========================================================
# VALID STATE TRANSITIONS
# =========================================================

VALID_TRANSITIONS = {

    # -----------------------------------
    # INITIAL FLOW
    # -----------------------------------

    "CREATED": [
        "AUTH_INITIATED",
        "FAILED"
    ],

    # -----------------------------------
    # AUTHORIZATION FLOW
    # -----------------------------------

    "AUTH_INITIATED": [
        "AUTHORIZED",
        "FAILED"
    ],

    # -----------------------------------
    # AUTHORIZED FLOW
    # -----------------------------------

    "AUTHORIZED": [
        "CAPTURED",
        "FAILED"
    ],

    # -----------------------------------
    # CAPTURED FLOW
    # -----------------------------------

    "CAPTURED": [
        "REFUNDED"
    ],

    # -----------------------------------
    # TERMINAL STATES
    # -----------------------------------

    "FAILED": [],

    "REFUNDED": []
}


# =========================================================
# EVENT -> STATE TRANSITIONS
# =========================================================

EVENT_TRANSITIONS = {

    # -----------------------------------
    # AUTH FLOW
    # -----------------------------------

    "START_AUTH": {
        "from": "CREATED",
        "to": "AUTH_INITIATED"
    },

    "AUTH_SUCCESS": {
        "from": "AUTH_INITIATED",
        "to": "AUTHORIZED"
    },

    "AUTH_FAILED": {
        "from": "AUTH_INITIATED",
        "to": "FAILED"
    },

    # -----------------------------------
    # PAYMENT CAPTURE
    # -----------------------------------

    "CAPTURE_PAYMENT": {
        "from": "AUTHORIZED",
        "to": "CAPTURED"
    },

    # -----------------------------------
    # PAYMENT FAILURE
    # -----------------------------------

    "PAYMENT_FAILED": {
        "from": "AUTHORIZED",
        "to": "FAILED"
    },

    # -----------------------------------
    # REFUND FLOW
    # -----------------------------------

    "REFUND_PAYMENT": {
        "from": "CAPTURED",
        "to": "REFUNDED"
    }
}


# =========================================================
# VALIDATE STATE TRANSITION
# =========================================================

def validate_transition(
    current_state: str,
    new_state: str
):

    allowed = VALID_TRANSITIONS.get(
        current_state,
        []
    )

    if new_state not in allowed:

        raise Exception(
            f"Invalid transition "
            f"from {current_state} "
            f"to {new_state}"
        )

    return True