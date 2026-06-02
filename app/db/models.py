import enum
import uuid

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    Float,
    Boolean
)

from sqlalchemy.sql import func

from sqlalchemy.types import Enum as SqlEnum

from ..database import Base


# =========================================================
# TRANSACTION STATES
# =========================================================

class TransactionState(str, enum.Enum):

    CREATED = "CREATED"

    AUTH_INITIATED = "AUTH_INITIATED"

    AUTHORIZED = "AUTHORIZED"

    CAPTURED = "CAPTURED"

    FAILED = "FAILED"

    REFUNDED = "REFUNDED"


# =========================================================
# TRANSACTIONS
# =========================================================

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    merchant_order_id = Column(
        String,
        nullable=True
    )

    amount_paise = Column(
        BigInteger,
        nullable=False
    )

    currency = Column(
        String,
        default="INR"
    )

    state = Column(
        SqlEnum(TransactionState),
        nullable=False,
        default=TransactionState.CREATED
    )

    gateway = Column(
        String,
        nullable=True
    )

    gateway_reference = Column(
        String,
        nullable=True
    )

    gateway_payment_id = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    last_reconciled_at = Column(
        DateTime(timezone=True),
        nullable=True
    )


# =========================================================
# TRANSACTION STATE LOGS
# =========================================================

class TransactionStateLog(Base):

    __tablename__ = "transaction_state_logs"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    transaction_id = Column(
        String,
        ForeignKey("transactions.id"),
        nullable=False
    )

    from_state = Column(
        SqlEnum(TransactionState),
        nullable=False
    )

    to_state = Column(
        SqlEnum(TransactionState),
        nullable=False
    )

    event = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# =========================================================
# PROCESSED WEBHOOK EVENTS
# =========================================================

class ProcessedWebhookEvent(Base):

    __tablename__ = "processed_webhook_events"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    gateway = Column(
        String,
        nullable=False
    )

    event_id = Column(
        String,
        nullable=False
    )

    event_type = Column(
        String,
        nullable=False
    )

    payload_hash = Column(
        String,
        nullable=False
    )

    transaction_id = Column(
        String,
        ForeignKey("transactions.id"),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# =========================================================
# RECONCILIATION LOGS
# =========================================================

class ReconciliationLog(Base):

    __tablename__ = "reconciliation_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    transaction_id = Column(
        String,
        ForeignKey("transactions.id"),
        nullable=False
    )

    internal_status = Column(
        String,
        nullable=False
    )

    gateway_status = Column(
        String,
        nullable=False
    )

    discrepancy_found = Column(
        Boolean,
        default=False
    )

    discrepancy_type = Column(
        String,
        nullable=True
    )

    action_taken = Column(
        String,
        nullable=True
    )

    notes = Column(
        String,
        nullable=True
    )

    resolved = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# =========================================================
# PAYMENT ANOMALIES
# =========================================================

class PaymentAnomaly(Base):

    __tablename__ = "payment_anomalies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    transaction_id = Column(
        String,
        ForeignKey("transactions.id"),
        nullable=False
    )

    internal_status = Column(
        String,
        nullable=False
    )

    gateway_status = Column(
        String,
        nullable=False
    )

    issue_type = Column(
        String,
        nullable=False
    )

    severity = Column(
        String,
        default="HIGH"
    )

    resolved = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# =========================================================
# GATEWAY HEALTH METRICS
# =========================================================

class GatewayHealthMetric(Base):

    __tablename__ = "gateway_health_metrics"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    gateway = Column(
        String,
        nullable=False
    )

    success_rate = Column(
        Float,
        nullable=False
    )

    avg_latency_ms = Column(
        Float,
        nullable=False
    )

    total_requests = Column(
        Integer,
        default=0
    )

    failed_requests = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )