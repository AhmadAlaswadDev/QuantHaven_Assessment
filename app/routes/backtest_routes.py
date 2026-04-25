from fastapi import APIRouter
from app.controllers import backtest_controller

router = APIRouter(prefix="/backtest", tags=["Backtest"])

router.add_api_route("/", backtest_controller.index, methods=["GET"])
router.add_api_route("/run", backtest_controller.run, methods=["POST"])