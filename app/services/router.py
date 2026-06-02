from app.services.gateway_health import (
    gateway_metrics
)


def select_gateway(amount: float):

    # Avoid unhealthy gateways

    razorpay_failures = gateway_metrics[
        "razorpay"
    ]["failure"]

    stripe_failures = gateway_metrics[
        "stripe"
    ]["failure"]

    payu_failures = gateway_metrics[
        "payu"
    ]["failure"]

    # If Razorpay unhealthy → use Stripe

    if razorpay_failures >= 3:
        return "stripe"

    # If Stripe unhealthy → use PayU

    if stripe_failures >= 3:
        return "payu"

    # Normal routing logic

    if amount < 1000:
        return "razorpay"

    return "stripe"