from fastapi import Request, HTTPException

async def validate_webhook(request: Request):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    #  validate payload security, check for a secret token in headers