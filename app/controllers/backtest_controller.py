from fastapi import HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import pandas as pd
import yfinance as yf
from app.requests.backtest_run_post_request import BackTestRunPostRequest


templates = Jinja2Templates(directory="app/templates")


class BacktestRunRequest(BaseModel):
    symbol: str = Field(default="BTC-USD", min_length=2)
    period: str = Field(default="30d")
    interval: str = Field(default="1h")


async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="backtest.html",
        context={}
    )


def run(data: BackTestRunPostRequest) -> dict:
    symbol = f"{data.coin}-{data.currency}"
    fast_ema = data.fast_ema
    slow_ema = data.slow_ema

    if fast_ema >= slow_ema:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "message": "Fast EMA must be less than Slow EMA"
            }
        )

    try:
        df = yf.download(
            tickers=symbol,
            period=data.period,
            interval=data.interval,
            progress=False,
            auto_adjust=True
        )

        if df.empty:
            raise ValueError("No market data found for this symbol or period")

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()

        close_col = "Close"

        df["ema_fast"] = df[close_col].ewm(span=fast_ema, adjust=False).mean()
        df["ema_slow"] = df[close_col].ewm(span=slow_ema, adjust=False).mean()

        df["previous_ema_fast"] = df["ema_fast"].shift(1)
        df["previous_ema_slow"] = df["ema_slow"].shift(1)

        trades = []
        position = None

        total_return = 0
        winning_trades = 0
        equity = 100
        peak = 100
        max_drawdown = 0

        for _, row in df.iterrows():
            price = float(row[close_col])
            time_value = str(row.iloc[0])

            bullish_cross = (
                row["previous_ema_fast"] <= row["previous_ema_slow"]
                and row["ema_fast"] > row["ema_slow"]
            )

            bearish_cross = (
                row["previous_ema_fast"] >= row["previous_ema_slow"]
                and row["ema_fast"] < row["ema_slow"]
            )

            if bullish_cross and position is None:
                position = {
                    "entry_time": time_value,
                    "entry_price": price
                }

            elif bearish_cross and position is not None:
                entry_price = position["entry_price"]

                profit = price - entry_price
                return_pct = (profit / entry_price) * 100

                entry_time_dt = pd.to_datetime(position["entry_time"])
                exit_time_dt = pd.to_datetime(time_value)

                duration_hours = (exit_time_dt - entry_time_dt).total_seconds() / 3600

                trade = {
                    "entry_time": position["entry_time"],
                    "exit_time": time_value,
                    "duration": round(duration_hours, 1),
                    "entry_price": round(entry_price, 2),
                    "exit_price": round(price, 2),
                    "profit": round(profit, 2),
                    "return_pct": round(return_pct, 2)
                }

                trades.append(trade)

                total_return += return_pct

                if profit > 0:
                    winning_trades += 1

                equity *= (1 + return_pct / 100)
                peak = max(peak, equity)
                drawdown = ((equity - peak) / peak) * 100
                max_drawdown = min(max_drawdown, drawdown)

                position = None

        number_of_trades = len(trades)
        win_rate = (winning_trades / number_of_trades * 100) if number_of_trades else 0

        result = {
            "symbol": symbol,
            "period": data.period,
            "interval": data.interval,
            "strategy": f"EMA {fast_ema}/{slow_ema} Crossover",
            "metrics": {
                "total_return": round(total_return, 2),
                "win_rate": round(win_rate, 2),
                "max_drawdown": round(max_drawdown, 2),
                "number_of_trades": number_of_trades
            },
            "trades": trades
        }

        return {
            "success": True,
            "message": "Backtest completed successfully",
            "payload": result
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "message": str(e)
            }
        )