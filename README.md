# QuantHaven Backtest Assessment

## Overview

This project is a simple full-stack application that demonstrates:

* EMA Crossover Backtesting (9/21 or configurable)
* Webhook Signal Ingestion
* Basic Trade Simulation and Reporting

The system uses historical market data to simulate how a trading strategy would perform.

---

## Features

### 1. Backtesting (EMA Crossover)

* Uses EMA Fast / EMA Slow (default: 9 / 21)
* Runs on historical OHLCV data (via yfinance)
* Generates simulated trades
* Calculates:

  * Total Return
  * Win Rate
  * Max Drawdown
  * Number of Trades

### 2. Webhook Endpoint

* Accepts POST signals (symbol, side, qty, price)
* Validates input
* Logs signals
* Simulates execution

### 3. UI

* Interactive form (Tailwind + jQuery)
* Dynamic backtest execution (AJAX)
* Trades table with:

  * Entry / Exit Time
  * Duration
  * Profit
* Download results as JSON

---

## Routes

### Webhook

```
POST /webhook/
```

### Backtest Page

```
GET /backtest/
```

### Run Backtest

```
POST /backtest/run
```

---

## How to Run

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start server

```bash
uvicorn app.main:app --reload
```

### 4. Open in browser

```
http://127.0.0.1:8000/backtest/
```

---

## Notes

* Trades are simulated based on historical data
* This is a backtesting system, not live trading
* Only USD pairs are supported (e.g., BTC-USD)

---

## Tech Stack

* FastAPI
* Pandas
* yfinance
* Tailwind CSS
* jQuery