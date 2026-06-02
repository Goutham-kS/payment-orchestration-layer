from uuid import uuid4

from sqlalchemy.orm import Session

from app.db.models import (
    Transaction,
    TransactionState,
    TransactionStateLog
)

from app.core.state_machine import (
    EVENT_TRANSITIONS,
    validate_transition
)

from app.services.router import (
    select_gateway
)

from app.services.mock_gateway_service import (
    process_razorpay_payment,
    process_stripe_payment,
)

from app.services.gateway_health import (
    record_gateway_success,
    record_gateway_failure,
)

from app.core.exceptions import (
    GatewayTimeoutError,
    GatewayFailedError,
)

from app.core.circuit_breaker import (
    CircuitBreaker,
)


# =========================================================
# CIRCUIT BREAKERS
# =========================================================

gateway_breakers = {
    "razorpay": CircuitBreaker(),
    "stripe": CircuitBreaker(),
}


# =========================================================
# FAILOVER GATEWAYS
# =========================================================

BACKUP_GATEWAYS = {
    "razorpay": "stripe",
    "stripe": "razorpay",
}


# =========================================================
# APPLY STATE MACHINE EVENT
# =========================================================

def apply_event(
    db: Session,
    txn: Transaction,
    event: str
):

    # -----------------------------------
    # Validate Event
    # -----------------------------------

    if event not in EVENT_TRANSITIONS:

        raise Exception(
            f"Unknown event: {event}"
        )

    rule = EVENT_TRANSITIONS[event]

    # -----------------------------------
    # Validate Current State
    # -----------------------------------

    if txn.state != rule["from"]:

        raise Exception(
            f"Invalid event {event} "
            f"from state {txn.state}"
        )

    new_state = rule["to"]

    # -----------------------------------
    # Validate Transition
    # -----------------------------------

    validate_transition(
        txn.state,
        new_state
    )

    # -----------------------------------
    # Immutable Audit Log
    # -----------------------------------

    log = TransactionStateLog(
        id=str(uuid4()),
        transaction_id=txn.id,
        from_state=txn.state,
        to_state=new_state,
        event=event,
    )

    db.add(log)

    # -----------------------------------
    # Apply State Change
    # -----------------------------------

    txn.state = new_state

    db.commit()

    db.refresh(txn)

    return txn


# =========================================================
# WEBHOOK HELPERS
# =========================================================

def mark_transaction_captured(
    db: Session,
    txn: Transaction
):

    txn.state = TransactionState.CAPTURED

    db.commit()

    db.refresh(txn)

    return txn


def mark_transaction_failed(
    db: Session,
    txn: Transaction
):

    txn.state = TransactionState.FAILED

    db.commit()

    db.refresh(txn)

    return txn


def mark_transaction_refunded(
    db: Session,
    txn: Transaction
):

    txn.state = TransactionState.REFUNDED

    db.commit()

    db.refresh(txn)

    return txn


# =========================================================
# PHASE 5 PAYMENT ORCHESTRATION
# =========================================================

async def process_payment(
    amount: float,
    headers: dict | None = None
):

    if headers is None:
        headers = {}

    # -----------------------------------
    # Step 1 - Select Gateway
    # -----------------------------------

    gateway = select_gateway(amount)

    breaker = gateway_breakers[gateway]

    # -----------------------------------
    # Step 2 - Circuit Breaker Check
    # -----------------------------------

    if not breaker.can_execute():

        gateway = BACKUP_GATEWAYS[gateway]

    try:

        # -----------------------------------
        # Step 3 - Process Payment
        # -----------------------------------

        if gateway == "razorpay":

            response = await process_razorpay_payment(
                headers
            )

        elif gateway == "stripe":

            response = await process_stripe_payment(
                headers
            )

        else:

            raise Exception(
                "Unsupported gateway"
            )

        # -----------------------------------
        # Step 4 - Record Success
        # -----------------------------------

        breaker.record_success()

        record_gateway_success(
            gateway
        )

        return {
            "success": True,
            "selected_gateway": gateway,
            "failover": False,
            "gateway_response": response
        }

    except (
        GatewayTimeoutError,
        GatewayFailedError,
        Exception
    ):

        # -----------------------------------
        # Step 5 - Record Failure
        # -----------------------------------

        breaker.record_failure()

        record_gateway_failure(
            gateway
        )

        # -----------------------------------
        # Step 6 - Select Backup Gateway
        # -----------------------------------

        backup_gateway = BACKUP_GATEWAYS.get(
            gateway
        )

        if not backup_gateway:

            return {
                "success": False,
                "message": "No backup gateway available"
            }

        # -----------------------------------
        # Step 7 - Retry With Backup Gateway
        # -----------------------------------

        if backup_gateway == "razorpay":

            backup_response = await process_razorpay_payment(
                headers
            )

        elif backup_gateway == "stripe":

            backup_response = await process_stripe_payment(
                headers
            )

        else:

            raise Exception(
                "Unsupported backup gateway"
            )

        return {
            "success": True,
            "selected_gateway": backup_gateway,
            "failover": True,
            "gateway_response": backup_response
        }