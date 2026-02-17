import finnhub
from datetime import datetime
import pandas as pd
client= finnhub.Client(api_key="d617g2pr01qjrruh84b0d617g2pr01qjrruh84bg")



while True:
    s=input("Ingrese el stock que desea visualizar: ").strip().upper()

    if client.quote(s)["c"]==0:
        print("El stock no existe")

    else:
        data=client.quote(s)
        
        precio=data["c"]
        cambio=data["d"]
        porcentaje=data["dp"]
        open=data["o"]
        fecha=str(datetime.fromtimestamp(data["t"],tz=None))
        dia,hora=fecha.split(" ")

        df=pd.DataFrame({
            "Fecha":[dia],
            "Hora":[hora],
            "Precio":[precio],
            "Cambio":[cambio],
            "Porcentaje":[porcentaje],
            "Open":[open]
            })
        
        file=f"{s}.csv"
        df.to_csv(file,mode="a",index=False,header=not pd.io.common.file_exists(file))