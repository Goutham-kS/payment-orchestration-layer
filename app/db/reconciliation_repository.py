from app.db.models import (
    ReconciliationLog,
    PaymentAnomaly
)


class ReconciliationRepository:

    # =====================================================
    # CREATE RECONCILIATION LOG
    # =====================================================

    @staticmethod
    def create_log(
        db,
        transaction_id,
        internal_status,
        gateway_status,
        discrepancy_found=False,
        discrepancy_type=None,
        action_taken=None,
        notes=None
    ):

        log = ReconciliationLog(
            transaction_id=transaction_id,
            internal_status=internal_status,
            gateway_status=gateway_status,
            discrepancy_found=discrepancy_found,
            discrepancy_type=discrepancy_type,
            action_taken=action_taken,
            notes=notes
        )

        db.add(log)

        db.commit()

        db.refresh(log)

        return log

    # =====================================================
    # CREATE PAYMENT ANOMALY
    # =====================================================

    @staticmethod
    def create_anomaly(
        db,
        transaction_id,
        internal_status,
        gateway_status,
        issue_type,
        severity="HIGH"
    ):

        anomaly = PaymentAnomaly(
            transaction_id=transaction_id,
            internal_status=internal_status,
            gateway_status=gateway_status,
            issue_type=issue_type,
            severity=severity
        )

        db.add(anomaly)

        db.commit()

        db.refresh(anomaly)

        return anomaly

    # =====================================================
    # GET ALL RECONCILIATION LOGS
    # =====================================================

    @staticmethod
    def get_all_logs(db):

        return db.query(
            ReconciliationLog
        ).all()

    # =====================================================
    # GET LOGS BY TRANSACTION
    # =====================================================

    @staticmethod
    def get_logs_by_transaction(
        db,
        transaction_id
    ):

        return db.query(
            ReconciliationLog
        ).filter(
            ReconciliationLog.transaction_id == transaction_id
        ).all()

    # =====================================================
    # GET ALL ANOMALIES
    # =====================================================

    @staticmethod
    def get_all_anomalies(db):

        return db.query(
            PaymentAnomaly
        ).all()

    # =====================================================
    # GET UNRESOLVED ANOMALIES
    # =====================================================

    @staticmethod
    def get_unresolved_anomalies(db):

        return db.query(
            PaymentAnomaly
        ).filter(
            PaymentAnomaly.resolved == False
        ).all()

    # =====================================================
    # MARK ANOMALY AS RESOLVED
    # =====================================================

    @staticmethod
    def resolve_anomaly(
        db,
        anomaly_id
    ):

        anomaly = db.query(
            PaymentAnomaly
        ).filter(
            PaymentAnomaly.id == anomaly_id
        ).first()

        if not anomaly:
            return None

        anomaly.resolved = True

        db.commit()

        db.refresh(anomaly)

        return anomaly