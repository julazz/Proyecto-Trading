import finnhub
from datetime import datetime
import pandas as pd
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor
from scipy.stats import linregress
import mplfinance as mpf
import matplotlib.pyplot as plt

client = finnhub.Client(api_key="d617g2pr01qjrruh84b0d617g2pr01qjrruh84bg")


def call(symbol):
    data = client.quote(symbol)

    if data["c"] == 0:
        print(f"{symbol}: El stock no existe")
        return

    precio = data["c"]
    cambio = data["d"]
    porcentaje = data["dp"]
    open_price = data["o"]
    fecha = str(datetime.fromtimestamp(data["t"], tz=None))
    dia, hora = fecha.split(" ")

    df = pd.DataFrame({
        "Fecha": [dia],
        "Hora": [hora],
        "Precio": [precio],
        "Cambio": [cambio],
        "Porcentaje": [porcentaje],
        "Open": [open_price]
    })

    file = f"{symbol}.csv"

    if pd.io.common.file_exists(file):
        last = pd.read_csv(file).tail(1)
        last_fecha = last["Fecha"].values[0]
        last_hora = last["Hora"].values[0]

        if last_fecha == dia and last_hora == hora:
            print(f"{symbol}: dato duplicado, no guardado")
            return

    df.to_csv(
        file,
        mode="a",
        index=False,
        header=not pd.io.common.file_exists(file)
    )

    print(f"{symbol} actualizado")


def analyze(symbol):
    file = f"{symbol}.csv"
    df = pd.read_csv(file)
    prices = df["Precio"]
    n = len(prices)

    print(f"\n{'='*40}")
    print(f"  ANALYiIS: {symbol} ({n} datos)")
    print(f"{'='*40}")

    # 1. TREND — Linear Regression Slope + R²
    slope, _, r_value, p_value, _ = linregress(range(n), prices)
    r2 = r_value ** 2
    trend_label = "Uptrend" if slope > 0 else "Downtrend"
    trend_strength = "strong" if r2 > 0.7 else "moderate" if r2 > 0.3 else "weak"
    print(f"\n[1] Trend (Linear Regression)")
    print(f"    Direction : {trend_label}")
    print(f"    Slope     : {slope:.6f} per tick")
    print(f"    R²        : {r2:.4f} ({trend_strength} trend)")
    print(f"    p-value   : {p_value:.4f} ({'significant' if p_value < 0.05 else 'not significant'})")

    # 2. VOLATILITY — Rolling Std Dev
    window = 12  # 12 x 5s = 1 min
    rolling_std = prices.rolling(window=window).std()
    avg_vol = rolling_std.mean()
    max_vol = rolling_std.max()
    vol_label = "High" if avg_vol > prices.mean() * 0.003 else "Low"
    print(f"\n[2] Volatility (Rolling Std, window=1min)")
    print(f"    Avg volatility : {avg_vol:.4f}")
    print(f"    Max volatility : {max_vol:.4f}")
    print(f"    Classification : {vol_label}")

    # 3. MOMENTUM — Rate of Change (ROC)
    roc = prices.pct_change(periods=window) * 100
    avg_roc = roc.mean()
    max_roc = roc.max()
    min_roc = roc.min()
    print(f"\n[3] Momentum (ROC over 1min)")
    print(f"    Avg ROC : {avg_roc:.4f}%")
    print(f"    Max ROC : {max_roc:.4f}%")
    print(f"    Min ROC : {min_roc:.4f}%")

    # 4. ANOMALY DETECTION — Z-Score of Returns
    returns = prices.pct_change()
    zscore = (returns - returns.mean()) / returns.std()
    anomalies = df[zscore.abs() > 2.5].copy()
    anomalies["zscore"] = zscore[zscore.abs() > 2.5]
    print(f"\n[4] Anomaly Detection (Z-Score > 2.5)")
    print(f"    Anomalies found : {len(anomalies)}")
    if not anomalies.empty:
        worst = anomalies.loc[anomalies["zscore"].abs().idxmax()]
        print(f"    Largest spike   : z={worst['zscore']:.2f} at {worst['Fecha']} {worst['Hora']}")

    # 5. MOVING AVERAGE CROSSOVER
    df["ma_fast"] = prices.rolling(12).mean()   # 1 min
    df["ma_slow"] = prices.rolling(60).mean()   # 5 min
    df["signal"] = (df["ma_fast"] > df["ma_slow"]).astype(int)
    crossovers = df["signal"].diff().abs().sum()
    final_signal = "Bullish" if df["signal"].iloc[-1] == 1 else "Bearish"
    print(f"\n[5] MA Crossover (fast=1min, slow=5min)")
    print(f"    Crossovers      : {int(crossovers)}")
    print(f"    Final signal    : {final_signal}")

    # SUMMARY
    print(f"\n--- PATTERN SUMMARY ---")
    if r2 > 0.3 and slope > 0:
        pattern = "Uptrend"
    elif r2 > 0.3 and slope < 0:
        pattern = "Downtrend"
    elif len(anomalies) > 3:
        pattern = "Volatile with anomalies"
    else:
        pattern = "Sideways / choppy"
    print(f"    Detected pattern: {pattern}")
    print(f"    Volatility      : {vol_label}")
    print(f"    Signal          : {final_signal}")

    return df


# ---- INPUT MULTIPLE STOCKS ----
stocks = input(
    "Ingrese los stocks separados por coma (ej: AAPL,MSFT,GOOGL): "
).strip().upper().split(",")

stocks = [s.strip() for s in stocks]

t = int(input("Ingrese la duracion de ejecucion en segundos: "))

start_time = time.time()

while time.time() - start_time < t:
    with ThreadPoolExecutor(max_workers=len(stocks)) as executor:
        executor.map(call, stocks)
    time.sleep(5)

# ---- ANALYZE PATTERNS ----
analyzed = {}
for symbol in stocks:
    analyzed[symbol] = analyze(symbol)

# ---- GRAFICAR LOS DATOS ----
for symbol in stocks:
    file = f"{symbol}.csv"
    df = pd.read_csv(file)

    df["Datetime"] = pd.to_datetime(df["Fecha"] + " " + df["Hora"])
    df.set_index("Datetime", inplace=True)

    ohlc = df["Precio"].resample("1min").ohlc()
    mpf.plot(ohlc, type="candle", title=symbol, style="charles")