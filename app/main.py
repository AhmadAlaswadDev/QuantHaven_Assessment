from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from app.exceptions.handlers import http_exception_handler, validation_exception_handler ,internal_exception_handler
from app.routes import backtest_routes, webhook_routes

app = FastAPI(title="QuantHaven Assessment")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# routes
app.add_api_route("/", lambda: { "success": True, "message": "Welcome to QuantHaven API"}, methods=["GET"])
app.include_router(webhook_routes.router)
app.include_router(backtest_routes.router)

# execptions
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, internal_exception_handler)