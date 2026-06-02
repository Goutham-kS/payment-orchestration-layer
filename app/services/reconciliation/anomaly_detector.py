from app.db.reconciliation_repository import (
    ReconciliationRepository
)

class AnomalyDetector:

    def __init__(self):

        self.repository = ReconciliationRepository()

    async def detect(
        self,
        db,
        transaction,
        gateway_status
    ):

        internal_status = transaction.state.value

        # ============================================
        # CRITICAL CASE
        # Internal says CAPTURED
        # Gateway says FAILED
        # ============================================

        if (
            internal_status == "CAPTURED"
            and
            gateway_status == "FAILED"
        ):

            anomaly = self.repository.create_anomaly(
                db=db,
                transaction_id=transaction.id,
                internal_status=internal_status,
                gateway_status=gateway_status,
                issue_type="CAPTURED_TO_FAILED",
                severity="CRITICAL"
            )

            return {
                "anomaly_detected": True,
                "severity": "CRITICAL",
                "issue_type": "CAPTURED_TO_FAILED",
                "anomaly": anomaly
            }

        # ============================================
        # SETTLEMENT MISSING
        # ============================================

        if (
            internal_status == "AUTHORIZED"
            and
            gateway_status == "FAILED"
        ):

            anomaly = self.repository.create_anomaly(
                db=db,
                transaction_id=transaction.id,
                internal_status=internal_status,
                gateway_status=gateway_status,
                issue_type="SETTLEMENT_MISSING",
                severity="HIGH"
            )

            return {
                "anomaly_detected": True,
                "severity": "HIGH",
                "issue_type": "SETTLEMENT_MISSING",
                "anomaly": anomaly
            }

        # ============================================
        # NO ANOMALY
        # ============================================

        return {
            "anomaly_detected": False
        }