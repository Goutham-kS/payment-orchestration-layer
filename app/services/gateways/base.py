from abc import ABC, abstractmethod

class PaymentGateway(ABC):

    @abstractmethod
    async def authorize(self, amount: int, headers: dict):
        pass

    @abstractmethod
    async def capture(self, transaction_id: str, headers: dict):
        pass