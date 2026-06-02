from fastapi import APIRouter
from fastapi import Request
from fastapi import Header
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.database import get_db

from app.services.webhooks.processor import (
    WebhookProcessor
)

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"]
)

# =========================================================
# WEBHOOK SECRETS
# =========================================================

RAZORPAY_WEBHOOK_SECRET = "razorpay_secret"

STRIPE_WEBHOOK_SECRET = "stripe_secret"


# =========================================================
# RAZORPAY WEBHOOK
# =========================================================

@router.post("/razorpay")
async def razorpay_webhook(
    request: Request,
    x_razorpay_signature: str = Header(None),
    db: Session = Depends(get_db)
):

    try:

        # -----------------------------------
        # Validate Header
        # -----------------------------------

        if not x_razorpay_signature:

            raise HTTPException(
                status_code=400,
                detail="Missing Razorpay signature header"
            )

        # -----------------------------------
        # Read Raw Payload
        # -----------------------------------

        payload = await request.body()

        # -----------------------------------
        # Process Webhook
        # -----------------------------------

        result = WebhookProcessor.process_razorpay_webhook(
            payload=payload,
            signature=x_razorpay_signature,
            secret=RAZORPAY_WEBHOOK_SECRET,
            db=db
        )

        return JSONResponse(
            status_code=200,
            content=result
        )

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================================================
# STRIPE WEBHOOK
# =========================================================

@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None),
    db: Session = Depends(get_db)
):

    try:

        # -----------------------------------
        # Validate Header
        # -----------------------------------

        if not stripe_signature:

            raise HTTPException(
                status_code=400,
                detail="Missing Stripe signature header"
            )

        # -----------------------------------
        # Read Raw Payload
        # -----------------------------------

        payload = await request.body()

        # -----------------------------------
        # Process Webhook
        # -----------------------------------

        result = WebhookProcessor.process_stripe_webhook(
            payload=payload,
            signature=stripe_signature,
            secret=STRIPE_WEBHOOK_SECRET,
            db=db
        )

        return JSONResponse(
            status_code=200,
            content=result
        )

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )