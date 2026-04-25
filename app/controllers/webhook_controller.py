from datetime import datetime, timezone
from fastapi import HTTPException
from app.helpers.file import append_json
from app.requests.webhool_post_request import WebhookPostRequest
from app.services.broker_service import mock_execute_trade


async def handle_post(data: WebhookPostRequest):
    payload = data.model_dump()

    signal_id = f'{payload["symbol"]}-{payload["side"]}-{payload["qty"]}-{payload["price"]}'

    signal = {
        "id": signal_id,
        **payload,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    try:
        append_json(
            "signals.json",
            signal,
            should_be_unique=True,
            unique_key="id"
        )

        execution = mock_execute_trade(signal)
        return {
            "success": True,
            "message": "Signal received and stored successfully",
            "payload": {
                "signal": signal,
                "execution": execution
            },
        }

    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail={
                "success": False,
                "message": str(e)
        }
    )

