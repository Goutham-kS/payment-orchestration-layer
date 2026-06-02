from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db import models
from app.db.models import Transaction, TransactionState

from app.core.state_machine import (
    EVENT_TRANSITIONS,
    validate_transition
)


# ==============================
# CREATE PAYMENT
# ==============================

def create_payment(
    db: Session,
    amount_rupees: int,
    merchant_order_id: str = None
):

    if amount_rupees <= 0:
        raise ValueError("Amount must be greater than 0")

    txn = Transaction(
        amount_paise=amount_rupees * 100,
        merchant_order_id=merchant_order_id,
        state=TransactionState.CREATED
    )

    db.add(txn)

    db.commit()

    db.refresh(txn)

    return txn


# ==============================
# GET TRANSACTION
# ==============================

def get_transaction(
    db: Session,
    txn_id: str
):

    return db.query(Transaction).filter(
        Transaction.id == txn_id
    ).first()


# ==============================
# APPLY EVENT
# ==============================

def apply_event(
    db: Session,
    txn_id: str,
    event: str
):

    try:

        # Lock row for concurrency safety
        txn = db.query(Transaction).filter(
            Transaction.id == txn_id
        ).with_for_update().first()

        if not txn:
            return None

        # Validate event exists
        if event not in EVENT_TRANSITIONS:
            raise Exception(f"Invalid event: {event}")

        rule = EVENT_TRANSITIONS[event]

        # Validate current state
        if txn.state != rule["from"]:
            raise Exception(
                f"Invalid event {event} from state {txn.state}"
            )

        new_state = rule["to"]

        # Double validation
        validate_transition(
            txn.state,
            new_state
        )

        # Create immutable audit log
        log = models.TransactionStateLog(
            transaction_id=txn.id,
            from_state=txn.state,
            to_state=new_state,
            event=event
        )

        db.add(log)

        # Apply state change
        txn.state = new_state

        # Commit atomically
        db.commit()

        db.refresh(txn)

        return txn

    except SQLAlchemyError as e:

        db.rollback()

        raise e