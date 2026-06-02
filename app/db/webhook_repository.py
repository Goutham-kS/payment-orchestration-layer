from sqlalchemy.orm import Session
from app.db.idempotency import IdempotencyKey

from app.db.models import (
    Transaction,
    ProcessedWebhookEvent
)


class WebhookRepository:

    @staticmethod
    def webhook_exists(
        db: Session,
    
        gateway: str,
        event_id: str
    ):

        return db.query(
            ProcessedWebhookEvent
        ).filter(
            ProcessedWebhookEvent.gateway == gateway,
            ProcessedWebhookEvent.event_id == event_id
        ).first()

    @staticmethod
    def save_processed_event(
        db: Session,
        gateway: str,
        event_id: str,
        event_type: str,
        payload_hash: str,
        transaction_id=None
    ):

        event = ProcessedWebhookEvent(
            gateway=gateway,
            event_id=event_id,
            event_type=event_type,
            payload_hash=payload_hash,
            transaction_id=transaction_id
        )

        db.add(event)
        db.commit()

        return event