from pydantic import BaseModel, Field
from typing import Literal

class WebhookPostRequest(BaseModel):
    symbol: str = Field(..., min_length=3)
    side: Literal["buy", "sell"]
    qty: float = Field(..., gt=0)
    price: float = Field(..., gt=0)