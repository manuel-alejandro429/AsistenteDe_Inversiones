
#Instalando el paquete de yfinance (Si es nesario, depende si el entorno no lo tiene por defecto)

!pip install yfinance

#Se importan todas las librerias necesarias

import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression

#Función para obtener datos historicos de un par de divisa específico
def obtener_datos_historicos(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data['Close']

#Nos ayuda a calcular la regresion lineal
def calcular_regresion_lineal(data):
    X = pd.DataFrame(data.index).astype(int)  # Convertir la fecha en valor numérico
    y = data.values.reshape(-1, 1)

    regresion = LinearRegression()
    regresion.fit(X, y)

    return regresion.coef_[0][0], regresion.intercept_[0]

#SE REALIZAN ALGUNAS PRUEBAS DE LAS FUNCIONES ANTERIORES. ----------------------------------------

# Parámetros de entrada
symbol = 'EURUSD=X'

# Obtener fechas
start_date = input("Ingrese la fecha de inicio (año-mes-día): ")
end_date = input("Ingrese la fecha de fin (año-mes-día): ")

# Obtener datos históricos
data = obtener_datos_historicos(symbol, start_date, end_date)
#Visualizamos los datos obtenidos a traves de la API de Yahoo Finance
print(data)

# Calcular regresión lineal
coeficiente, intercepto = calcular_regresion_lineal(data)


print("Coeficiente:", coeficiente)
print("Intercepto:", intercepto)
