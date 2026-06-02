from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Header
)

from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.crud import (
    get_transaction,
    create_payment,
    apply_event,
)

from app.services.transaction_service import process_payment

from app.services.idempotency_service import (
    IdempotencyService
)


router = APIRouter(
    prefix="/api/v1/payments",
    tags=["Payments"]
)


# ==============================
# DATABASE DEPENDENCY
# ==============================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==============================
# CREATE PAYMENT
# PHASE 6 - IDEMPOTENCY
# ==============================

@router.post("/")
async def create_payment_api(
    request: Request,
    amount: int,
    merchant_order_id: str = None,
    idempotency_key: str = Header(None),
    db: Session = Depends(get_db)
):

    # =========================
    # REQUIRE IDEMPOTENCY KEY
    # =========================

    if not idempotency_key:

        raise HTTPException(
            status_code=400,
            detail="Idempotency-Key header required"
        )

    # =========================
    # CREATE REQUEST HASH
    # =========================

    request_data = {
        "amount": amount,
        "merchant_order_id": merchant_order_id
    }

    request_hash = (
        IdempotencyService.generate_request_hash(
            request_data
        )
    )

    # =========================
    # CHECK EXISTING KEY
    # =========================

    existing = IdempotencyService.get_key(
        db,
        idempotency_key
    )

    # DUPLICATE REQUEST
    if existing:

        # REQUEST STILL PROCESSING
        if existing.status == "PROCESSING":

            raise HTTPException(
                status_code=409,
                detail="Request already processing"
            )

        # RETURN CACHED RESPONSE
        if existing.status == "COMPLETED":

            return existing.response_body

    # =========================
    # CREATE LOCK
    # =========================

    IdempotencyService.create_key(
        db,
        idempotency_key,
        request_hash
    )

    # =========================
    # PROCESS PAYMENT
    # =========================

    try:

        headers = dict(request.headers)

        result = await process_payment(
            amount=amount,
            headers=headers
        )

        # SAVE RESPONSE
        IdempotencyService.mark_completed(
            db,
            idempotency_key,
            result
        )

        return result

    except Exception as e:

        # MARK FAILED
        IdempotencyService.mark_failed(
            db,
            idempotency_key
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==============================
# START AUTH
# ==============================

@router.put("/{payment_id}/start-auth")
def start_auth(
    payment_id: str,
    db: Session = Depends(get_db)
):

    txn = get_transaction(db, payment_id)

    if not txn:

        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return apply_event(
        db,
        payment_id,
        "START_AUTH"
    )


# ==============================
# AUTH SUCCESS
# ==============================

@router.put("/{payment_id}/auth-success")
def mark_success(
    payment_id: str,
    db: Session = Depends(get_db)
):

    txn = get_transaction(db, payment_id)

    if not txn:

        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return apply_event(
        db,
        payment_id,
        "AUTH_SUCCESS"
    )


# ==============================
# AUTH FAILED
# ==============================

@router.put("/{payment_id}/auth-failed")
def mark_failed(
    payment_id: str,
    db: Session = Depends(get_db)
):

    txn = get_transaction(db, payment_id)

    if not txn:

        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return apply_event(
        db,
        payment_id,
        "AUTH_FAILED"
    )