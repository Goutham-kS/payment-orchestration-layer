from typing import Dict, Any


def extract_stripe_event(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize Stripe webhook payload into
    internal standardized structure.
    """

    data_object = payload.get("data", {}).get("object", {})

    return {
        "event_id": payload.get("id"),

        "event_type": payload.get("type"),

        "payment_intent": data_object.get("id"),

        "amount": data_object.get("amount"),

        "currency": data_object.get("currency"),

        "status": data_object.get("status"),

        "customer": data_object.get("customer"),

        "metadata": data_object.get("metadata", {}),

        "raw_payload": payload
    }


def get_stripe_target_state(event_type: str) -> str:
    """
    Convert Stripe webhook event type
    into internal transaction state.
    """

    event_state_map = {
        "payment_intent.succeeded": "CAPTURED",

        "payment_intent.payment_failed": "FAILED",

        "payment_intent.canceled": "FAILED",

        "charge.refunded": "REFUNDED",

        "charge.failed": "FAILED",
    }

    return event_state_map.get(event_type)


def is_supported_event(event_type: str) -> bool:
    """
    Check whether webhook event
    is supported by orchestration layer.
    """

    supported_events = {
        "payment_intent.succeeded",
        "payment_intent.payment_failed",
        "payment_intent.canceled",
        "charge.refunded",
        "charge.failed",
    }

    return event_type in supported_events