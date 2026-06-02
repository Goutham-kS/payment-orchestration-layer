import json

from sqlalchemy.orm import Session

from app.services.webhooks.verifier import (
    verify_razorpay_signature,
    verify_stripe_signature,
    generate_payload_hash
)

from app.services.webhooks.razorpay import (
    extract_razorpay_event
)

from app.services.webhooks.stripe import (
    extract_stripe_event,
    get_stripe_target_state,
    is_supported_event
)

from app.db.webhook_repository import (
    WebhookRepository
)

from app.core.webhook_events import (
    RAZORPAY_EVENT_STATE_MAP
)

from app.db.models import Transaction

from app.services.webhooks.handlers import (
    handle_payment_captured,
    handle_payment_failed
)


class WebhookProcessor:

    # =========================================================
    # RAZORPAY WEBHOOK PROCESSOR
    # =========================================================

    @staticmethod
    def process_razorpay_webhook(
        payload: bytes,
        signature: str,
        secret: str,
        db: Session
    ):

        # -----------------------------------
        # Verify Signature
        # -----------------------------------

        is_valid = verify_razorpay_signature(
            payload,
            signature,
            secret
        )

        if not is_valid:
            raise Exception("Invalid Razorpay webhook signature")

        # -----------------------------------
        # Parse Payload
        # -----------------------------------

        data = json.loads(payload)

        event_data = extract_razorpay_event(data)

        event_id = event_data["event_id"]
        event_type = event_data["event_type"]

        # -----------------------------------
        # Deduplication Check
        # -----------------------------------

        existing_event = WebhookRepository.webhook_exists(
            db,
            "razorpay",
            event_id
        )

        if existing_event:
            return {
                "status": "duplicate webhook"
            }

        # -----------------------------------
        # Find Transaction
        # -----------------------------------

        transaction = db.query(Transaction).filter(
            Transaction.gateway_payment_id ==
            event_data["payment_id"]
        ).first()

        if not transaction:
            raise Exception("Transaction not found")

        # -----------------------------------
        # Determine Target State
        # -----------------------------------

        target_state = RAZORPAY_EVENT_STATE_MAP.get(
            event_type
        )

        if not target_state:
            return {
                "status": "ignored unknown event"
            }

        # -----------------------------------
        # Out-of-order / duplicate handling
        # -----------------------------------

        if transaction.state == target_state:
            return {
                "status": "already processed"
            }

        # -----------------------------------
        # Process Event
        # -----------------------------------

        if target_state == "CAPTURED":

            handle_payment_captured(
                transaction,
                db
            )

        elif target_state == "FAILED":

            handle_payment_failed(
                transaction,
                db
            )

        # -----------------------------------
        # Save Processed Event
        # -----------------------------------

        WebhookRepository.save_processed_event(
            db=db,
            gateway="razorpay",
            event_id=event_id,
            event_type=event_type,
            payload_hash=generate_payload_hash(payload),
            transaction_id=transaction.id
        )

        return {
            "status": "processed"
        }

    # =========================================================
    # STRIPE WEBHOOK PROCESSOR
    # =========================================================

    @staticmethod
    def process_stripe_webhook(
        payload: bytes,
        signature: str,
        secret: str,
        db: Session
    ):

        # -----------------------------------
        # Verify Signature
        # -----------------------------------

        is_valid = verify_stripe_signature(
            payload,
            signature,
            secret
        )

        if not is_valid:
            raise Exception("Invalid Stripe webhook signature")

        # -----------------------------------
        # Parse Payload
        # -----------------------------------

        data = json.loads(payload)

        event_data = extract_stripe_event(data)

        event_id = event_data["event_id"]
        event_type = event_data["event_type"]

        # -----------------------------------
        # Supported Event Check
        # -----------------------------------

        if not is_supported_event(event_type):
            return {
                "status": "ignored unsupported event"
            }

        # -----------------------------------
        # Deduplication Check
        # -----------------------------------

        existing_event = WebhookRepository.webhook_exists(
            db,
            "stripe",
            event_id
        )

        if existing_event:
            return {
                "status": "duplicate webhook"
            }

        # -----------------------------------
        # Find Transaction
        # -----------------------------------

        transaction = db.query(Transaction).filter(
            Transaction.gateway_payment_id ==
            event_data["payment_intent"]
        ).first()

        if not transaction:
            raise Exception("Transaction not found")

        # -----------------------------------
        # Determine Target State
        # -----------------------------------

        target_state = get_stripe_target_state(
            event_type
        )

        if not target_state:
            return {
                "status": "ignored unknown state"
            }

        # -----------------------------------
        # Out-of-order / duplicate handling
        # -----------------------------------

        if transaction.state == target_state:
            return {
                "status": "already processed"
            }

        # -----------------------------------
        # Process Event
        # -----------------------------------

        if target_state == "CAPTURED":

            handle_payment_captured(
                transaction,
                db
            )

        elif target_state == "FAILED":

            handle_payment_failed(
                transaction,
                db
            )

        # -----------------------------------
        # Save Processed Event
        # -----------------------------------

        WebhookRepository.save_processed_event(
            db=db,
            gateway="stripe",
            event_id=event_id,
            event_type=event_type,
            payload_hash=generate_payload_hash(payload),
            transaction_id=transaction.id
        )

        return {
            "status": "processed"
        }