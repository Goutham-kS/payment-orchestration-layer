class GatewayError(Exception):
    pass


class GatewayTimeoutError(GatewayError):
    pass


class GatewayFailedError(GatewayError):
    pass
