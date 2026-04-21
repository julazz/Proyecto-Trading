🚀 Funcionalidades

📡 Recolección de datos
Obtiene precios en tiempo real usando Finnhub API
Guarda datos históricos en archivos .csv por símbolo
Evita duplicados por timestamp
Soporte para múltiples stocks en paralelo (multithreading)

📊 Análisis de mercado
El sistema ejecuta automáticamente:
1. Tendencia (Regresión lineal)
Dirección: Uptrend / Downtrend
Fuerza basada en R²
Significancia estadística (p-value)
2. Volatilidad
Desviación estándar móvil
Clasificación: alta / baja
3. Momentum
Rate of Change (ROC)
Identificación de cambios bruscos
4. Detección de anomalías
Z-score sobre retornos
Identificación de spikes extremos
5. Señales de trading
Cruce de medias móviles:
Rápida: 1 min
Lenta: 5 min
Señal final: Bullish / Bearish

🔎 Resumen automático
Clasificación general del comportamiento:
-Tendencia alcista
-Tendencia bajista
-Mercado lateral
-Alta volatilidad con anomalías

📉 Visualización
-Gráficos tipo candlestick
-Resampling automático a 1 minuto
-Uso de mplfinance


🧠 Roadmap (Machine Learning)
 🔲Modelos de predicción de precios 
 🔲Series temporales (ARIMA, LSTM)
 🔲Clasificación de señales de trading
 🔲Backtesting de estrategias
 🔲Optimización de hiperparámetros


⚙️ Instalación
git clone https://github.com/tu-usuario/trading-analyzer.gitcd trading-analyzerpip install -r requirements.txt


📦 Dependencias
-finnhub-python
-pandas
-numpy
-scipy
-mplfinance
-matplotlib


🔑 Configuración
Reemplaza tu API key de Finnhub en el código:
client = finnhub.Client(api_key="TU_API_KEY")


▶️ Uso
Ejecuta el script:
python main.py
Luego ingresa:
Ingrese los stocks separados por coma: AAPL,MSFT,GOOGLIngrese la duracion de ejecucion en segundos: 60

El sistema:
-Recolecta datos cada 5 segundos
-Guarda en CSV
-Analiza patrones automáticamente
-Genera gráficos


⚠️ Limitaciones actuales
-No usa datos OHLC reales (solo precio → reconstrucción)
-No hay persistencia avanzada (solo CSV)
-Sin backtesting
-Sin modelos predictivos aún


⚠️ Disclaimer
Este proyecto es únicamente educativo.
No constituye asesoría financiera.
El trading implica riesgo.


📌 Posibles mejoras
-Integrar datos OHLC reales
-Base de datos (SQLite / PostgreSQL)
-Dashboard (Streamlit / Dash)
- Integración con brokers


