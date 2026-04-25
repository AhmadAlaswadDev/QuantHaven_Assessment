from pydantic import BaseModel, Field
from typing import Literal

class BackTestRunPostRequest(BaseModel):
    coin: str
    currency: str
    period: Literal["7d", "30d", "60d", "90d"]
    interval: Literal["15m", "1h", "1d"]
    fast_ema: int = Field(default=9, gt=0)
    slow_ema: int = Field(default=21, gt=0)