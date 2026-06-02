from typing import Dict


def extract_razorpay_event(payload: Dict):

    return {
        "event_id": payload.get("payload", {})
                            .get("payment", {})
                            .get("entity", {})
                            .get("id"),

        "event_type": payload.get("event"),

        "payment_id": payload.get("payload", {})
                             .get("payment", {})
                             .get("entity", {})
                             .get("id"),

        "order_id": payload.get("payload", {})
                           .get("payment", {})
                           .get("entity", {})
                           .get("order_id"),

        "amount": payload.get("payload", {})
                         .get("payment", {})
                         .get("entity", {})
                         .get("amount"),

        "currency": payload.get("payload", {})
                           .get("payment", {})
                           .get("entity", {})
                           .get("currency")
    }