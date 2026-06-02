from datetime import datetime

from app.db.reconciliation_repository import (
    ReconciliationRepository
)


from app.services.reconciliation.gateway_poller import (
    GatewayPoller
)

from app.services.reconciliation.anomaly_detector import (
    AnomalyDetector
)


class ReconciliationEngine:

    def __init__(self):

        self.poller = GatewayPoller()

        self.detector = AnomalyDetector()

        self.repository = ReconciliationRepository()

    async def reconcile_transaction(
        self,
        db,
        transaction
    ):

        # ============================================
        # FETCH GATEWAY STATUS
        # ============================================

        gateway_response = await self.poller.fetch_payment_status(
            transaction.gateway,
            transaction.gateway_payment_id
        )

        gateway_status = gateway_response["status"]

        # ============================================
        # INTERNAL STATUS
        # ============================================

        internal_status = transaction.state.value

        discrepancy_found = (
            internal_status != gateway_status
        )

        action_taken = "NONE"

        # ============================================
        # DETECT ANOMALIES
        # ============================================

        anomaly_result = await self.detector.detect(
            db=db,
            transaction=transaction,
            gateway_status=gateway_status
        )

        if anomaly_result["anomaly_detected"]:

            action_taken = "ANOMALY_CREATED"

        # ============================================
        # AUTO FIX CASE
        # ============================================

        elif (
            internal_status == "AUTH_INITIATED"
            and
            gateway_status == "CAPTURED"
        ):

            transaction.state = "CAPTURED"

            transaction.last_reconciled_at = (
                datetime.utcnow()
            )

            db.commit()

            action_taken = "AUTO_CORRECTED"

        # ============================================
        # UPDATE RECONCILIATION TIMESTAMP
        # ============================================

        transaction.last_reconciled_at = (
            datetime.utcnow()
        )

        db.commit()

        # ============================================
        # CREATE RECONCILIATION LOG
        # ============================================

        self.repository.create_log(
            db=db,
            transaction_id=transaction.id,
            internal_status=internal_status,
            gateway_status=gateway_status,
            discrepancy_found=discrepancy_found,
            discrepancy_type=(
                "STATUS_MISMATCH"
                if discrepancy_found
                else None
            ),
            action_taken=action_taken,
            notes="Reconciliation completed"
        )

        # ============================================
        # RESPONSE
        # ============================================

        return {
            "transaction_id": transaction.id,
            "internal_status": internal_status,
            "gateway_status": gateway_status,
            "discrepancy_found": discrepancy_found,
            "action_taken": action_taken
        }