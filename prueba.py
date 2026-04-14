import pandas as pd
import random
from datetime import datetime, timedelta

TIMEFRAME_SECONDS = 5

START_TIME = datetime(2026, 3, 17, 14, 0, 0)
END_TIME   = datetime(2026, 3, 17, 15, 0, 0)

START_PRICE = {
    "NVDA": 180,
    "AAPL": 220,
    "GOOGL": 150
}

OPEN_PRICE = {
    "NVDA": 185.06,
    "AAPL": 223.10,
    "GOOGL": 148.50
}


def nvda_uptrend(price):
    drift = 0.04
    noise = random.uniform(-0.15, 0.25)
    return price + drift + noise


levels = [223, 225, 222, 228, 222, 224, 219]
speed = 0.35

def aapl_head_shoulders(step, price):

    phase = step // 8

    if phase >= len(levels):
        drift = random.uniform(-0.05, 0.05)
        return price + drift

    target = levels[phase]

    move = (target - price) * speed

    noise = random.uniform(-0.03, 0.03)

    return price + move + noise


PATTERN_START_G = 22
PATTERN_LEN_G = 24

def googl_double_bottom(step, price):

    drift = random.uniform(0.02, 0.06)

    if PATTERN_START_G <= step < PATTERN_START_G + PATTERN_LEN_G:

        phase = step - PATTERN_START_G

        if phase < 6:
            drift = -0.35      # first crash

        elif phase < 10:
            drift = 0.30       # bounce

        elif phase < 15:
            drift = -0.28      # second low

        else:
            drift = 0.45       # breakout

    noise = random.uniform(-0.02, 0.02)

    return price + drift + noise


def build_rows(symbol):

    rows = []
    now = START_TIME
    step = 0
    price = START_PRICE[symbol]

    while now <= END_TIME:

        if symbol == "NVDA":
            price = nvda_uptrend(price)

        elif symbol == "AAPL":
            price = aapl_head_shoulders(step, price)

        elif symbol == "GOOGL":
            price = googl_double_bottom(step, price)

        open_price = OPEN_PRICE[symbol]
        change = price - open_price
        pct = (change / open_price) * 100

        rows.append({
            "Fecha": now.strftime("%Y-%m-%d"),
            "Hora": now.strftime("%H:%M:%S"),
            "Precio": round(price, 2),
            "Cambio": round(change, 2),
            "Porcentaje": round(pct, 4),
            "Open": open_price
        })

        now += timedelta(seconds=TIMEFRAME_SECONDS)
        step += 1

    df = pd.DataFrame(rows)
    df.to_csv(f"{symbol}.csv", index=False)


for symbol in ["NVDA", "AAPL", "GOOGL"]:
    build_rows(symbol)

print("Generated only until 15:00:00 ✅")