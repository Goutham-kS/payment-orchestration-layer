from ..services.gateways.razorpay import RazorpayGateway
from ..services.gateways.stripe import StripeGateway
from ..services.gateways.payu import PayUGateway
from ..services.gateways.upi import UPIGateway


class GatewayRouter:

    def get_gateway(self, gateway_name: str):

        gateways = {
            "razorpay": RazorpayGateway(),
            "stripe": StripeGateway(),
            "payu": PayUGateway(),
            "upi": UPIGateway(),
        }

        return gateways[gateway_name]