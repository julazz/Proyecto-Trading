import finnhub
from datetime import datetime
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor

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
    df.to_csv(
        file,
        mode="a",
        index=False,
        header=not pd.io.common.file_exists(file)
    )

    print(f"{symbol} actualizado")


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