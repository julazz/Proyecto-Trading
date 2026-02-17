import finnhub
from datetime import datetime
client= finnhub.Client(api_key="d617g2pr01qjrruh84b0d617g2pr01qjrruh84bg")

#print(datetime.fromtimestamp(client.quote("NVDA")["t"],tz=None))
print(client.quote("NVDAFSADS"))

while True:
    s=input("Ingrese el stock que desea visualizar: ").strip().upper()
    if client.quote(s)["c"]==0:
        print("El stock no existe")
    else:
        print(client.quote(s))