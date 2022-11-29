from pydantic import BaseModel


class PaymentBody(BaseModel):

    amount: float
