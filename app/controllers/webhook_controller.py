from app.requests.webhool_post_request import WebhookPostRequest


async def handle_post(data: WebhookPostRequest):

    return {"success": True, "message": "Webhook processed", "data": data}