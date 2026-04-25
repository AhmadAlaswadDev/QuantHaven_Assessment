from fastapi import APIRouter, Depends
from app.middleware.webhook_middleware import validate_webhook
from app.controllers import webhook_controller
from app.requests.webhool_post_request import WebhookPostRequest

router = APIRouter(prefix="/webhook", tags=["Webhook"])


@router.post("/")
async def receive_webhook(
    data: WebhookPostRequest,
    _: None = Depends(validate_webhook)
):
    return await webhook_controller.handle_post(data)