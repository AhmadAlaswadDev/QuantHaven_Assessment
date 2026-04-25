from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.exceptions.handlers import http_exception_handler, validation_exception_handler ,internal_exception_handler
from app.routes import webhook_routes

app = FastAPI(title="QuantHaven Assessment")


# routes
app.add_api_route("/", lambda: { "success": True, "message": "Welcome to QuantHaven API"}, methods=["GET"])
app.include_router(webhook_routes.router)


# execptions
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, internal_exception_handler)