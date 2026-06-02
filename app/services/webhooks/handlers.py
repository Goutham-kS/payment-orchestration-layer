from sqlalchemy.orm import Session

from app.db.models import (
    Transaction,
    TransactionState
)


# =========================================================
# HANDLE PAYMENT CAPTURED
# =========================================================

def handle_payment_captured(
    transaction: Transaction,
    db: Session
):

    transaction.state = TransactionState.CAPTURED

    db.commit()

    db.refresh(transaction)

    return transaction


# =========================================================
# HANDLE PAYMENT FAILED
# =========================================================

def handle_payment_failed(
    transaction: Transaction,
    db: Session
):

    transaction.state = TransactionState.FAILED

    db.commit()

    db.refresh(transaction)

    return transaction


# =========================================================
# HANDLE PAYMENT REFUNDED
# =========================================================

def handle_payment_refunded(
    transaction: Transaction,
    db: Session
):

    transaction.state = TransactionState.REFUNDED

    db.commit()

    db.refresh(transaction)

    return transaction