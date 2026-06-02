from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.db.models import (
    Transaction
)

from app.db.reconciliation_repository import (
    ReconciliationRepository
)

from app.services.reconciliation.engine import (
    ReconciliationEngine
)

from app.services.reconciliation.poller import (
    ReconciliationPoller
)


router = APIRouter(
    prefix="/reconciliation",
    tags=["Reconciliation"]
)


# =====================================================
# MANUAL SINGLE TRANSACTION RECONCILIATION
# =====================================================

@router.post("/trigger/{transaction_id}")
async def reconcile_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
):

    transaction = db.query(
        Transaction
    ).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:

        return {
            "success": False,
            "message": "Transaction not found"
        }

    engine = ReconciliationEngine()

    result = await engine.reconcile_transaction(
        db=db,
        transaction=transaction
    )

    return {
        "success": True,
        "result": result
    }


# =====================================================
# RECONCILE ALL TRANSACTIONS
# =====================================================

@router.post("/run-all")
async def run_reconciliation():

    results = await ReconciliationPoller.run()

    return {
        "success": True,
        "total_processed": len(results),
        "results": results
    }


# =====================================================
# GET ALL RECONCILIATION LOGS
# =====================================================

@router.get("/logs")
def get_reconciliation_logs(
    db: Session = Depends(get_db)
):

    logs = (
        ReconciliationRepository
        .get_all_logs(db)
    )

    return {
        "success": True,
        "count": len(logs),
        "logs": logs
    }


# =====================================================
# GET ALL ANOMALIES
# =====================================================

@router.get("/anomalies")
def get_anomalies(
    db: Session = Depends(get_db)
):

    anomalies = (
        ReconciliationRepository
        .get_all_anomalies(db)
    )

    return {
        "success": True,
        "count": len(anomalies),
        "anomalies": anomalies
    }


# =====================================================
# GET UNRESOLVED ANOMALIES
# =====================================================

@router.get("/anomalies/unresolved")
def get_unresolved_anomalies(
    db: Session = Depends(get_db)
):

    anomalies = (
        ReconciliationRepository
        .get_unresolved_anomalies(db)
    )

    return {
        "success": True,
        "count": len(anomalies),
        "anomalies": anomalies
    }


# =====================================================
# RESOLVE ANOMALY
# =====================================================

@router.put("/anomalies/{anomaly_id}/resolve")
def resolve_anomaly(
    anomaly_id: int,
    db: Session = Depends(get_db)
):

    anomaly = (
        ReconciliationRepository
        .resolve_anomaly(
            db=db,
            anomaly_id=anomaly_id
        )
    )

    if not anomaly:

        return {
            "success": False,
            "message": "Anomaly not found"
        }

    return {
        "success": True,
        "message": "Anomaly resolved",
        "anomaly": anomaly
    }