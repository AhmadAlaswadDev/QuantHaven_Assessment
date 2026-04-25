import uuid
from datetime import datetime, timezone

from app.helpers.file import append_json


def mock_execute_trade(signal: dict) -> dict:

    total = signal["qty"] * signal["price"]
    trade =  {
        "order_id": str(uuid.uuid4()),
        "execution": "completed",
        "symbol": signal["symbol"],
        "side": signal["side"],
        "qty": signal["qty"],
        "price": signal["price"],
        "total": total,
        "signal_id": signal["id"],
        "executed_at": datetime.now(timezone.utc).isoformat()
    }
    
    append_json(
        "trades.json",
        trade,
        should_be_unique=False,
    )

    return trade