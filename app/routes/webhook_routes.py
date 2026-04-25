from fastapi import APIRouter, Depends
from app.middleware.webhook_middleware import validate_webhook
from app.controllers import webhook_controller

router = APIRouter(prefix="/webhook", tags=["Webhook"])

@router.post("/")
async def receive_webhook(data = Depends(validate_webhook)):
    return await webhook_controller.handle_post(data)