class GatewayPoller:

    async def fetch_payment_status(
        self,
        gateway_name,
        gateway_payment_id
    ):

        gateway_name = gateway_name.lower()

        mock_gateway_responses = {

            "razorpay": {
                "gateway": "razorpay",
                "payment_id": gateway_payment_id,
                "status": "CAPTURED"
            },

            "stripe": {
                "gateway": "stripe",
                "payment_id": gateway_payment_id,
                "status": "FAILED"
            },

            "payu": {
                "gateway": "payu",
                "payment_id": gateway_payment_id,
                "status": "PENDING"
            },

            "upi": {
                "gateway": "upi",
                "payment_id": gateway_payment_id,
                "status": "CAPTURED"
            }
        }

        response = mock_gateway_responses.get(
            gateway_name
        )

        if not response:

            return {
                "gateway": gateway_name,
                "payment_id": gateway_payment_id,
                "status": "FAILED",
                "error": "Unsupported gateway"
            }

        return response