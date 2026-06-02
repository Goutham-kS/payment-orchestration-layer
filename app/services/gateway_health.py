gateway_metrics = {
    "razorpay": {
        "success": 0,
        "failure": 0
    },

    "stripe": {
        "success": 0,
        "failure": 0
    },

    "payu": {
        "success": 0,
        "failure": 0
    },

    "upi": {
        "success": 0,
        "failure": 0
    }
}


def record_gateway_success(gateway: str):

    gateway_metrics[gateway]["success"] += 1


def record_gateway_failure(gateway: str):

    gateway_metrics[gateway]["failure"] += 1


def get_gateway_health():

    return gateway_metrics