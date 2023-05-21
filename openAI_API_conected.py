
#Instalando el paquete de yfinance-openai (Si es nesario, depende si el entorno no lo tiene por defecto)

#!pip install yfinance
#!pip install openai

#Se importan las librerias necesarias

import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import requests
import json
import openai


#Función para obtener datos historicos de un par de divisa específico
def obtener_datos_historicos(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data['Close']

#Nos ayuda a calcular la regresion lineal
def calcular_regresion_lineal(data):
    X = pd.to_numeric(data.index, errors='coerce').astype(int).values.reshape(-1, 1)
    #X = pd.to_numeric(data.index, errors='coerce').astype(int)
    #X = pd.DataFrame(data.index).to_numeric(int)  # Convertir la fecha en valor numérico
    #X = pd.DataFrame(data.index).astype(int)  # Convertir la fecha en valor numérico
    y = data.values.reshape(-1, 1)
    regresion = LinearRegression()
    regresion.fit(X, y)

    return regresion.coef_[0][0], regresion.intercept_[0]

#Función que permite darle contexto pertienente a la IA, segun la función para lo que se vaya a usar.
#En este caso, la finalidad es el análisis del mercado para EURUSD, por ello se le brindan algunos indicadores y demas.
def contextoIA  (timeStart,timeEnd,regresion,pmiUSD_prevision,pmiUSD_actual,pmiEuro_prevision,pmiEuro_actual,ipcEuro_prevision,ipcEuro_actual):

    tiempo_analizado = 'Se analizó la divisa EUR/USD desde:' + str(timeStart) + ', hasta: ' + str(timeEnd)
    regresion_lineal = 'Coeficiente de regresion lineal en el rango de tiempo analizado = ' + str(regresion)
    pmiUSD_zona = 'Valor prevision del PMI de Estados Unidos = ' + str(pmiUSD_prevision) + ', valor actual del PMI de Estados Unidos = ' + str(pmiUSD_actual)
    pmiEuro_zona = 'Valor prevision del PMI de la euro zona = ' + str(pmiEuro_prevision) + ', valor actual del PMI de la euro zona = ' + str(pmiEuro_actual)
    ipcEuro_zona = 'Porcentaje prevision del IPC de la euro zona = ' + str(ipcEuro_prevision) + '%, Porcentaje actual del IPC de la euro zona = ' + str(ipcEuro_actual) +'%'
    #El  siguiente parametro es para que la IA asuma un rol/personalidad.
    personalidad = '''Soy experto en el trading, incluyendo el análisis fundamental y técnico, tengo puntos de vista objetivos y
                      concretos. Mi mision es revisar tus especulaciónes del mercado del EUR/USD, basandome en los siguientes
                      parámetros: rango de tiempo analizado, regresion lineal de los datos, noticias económicas, etc. Al revisar tu
                      especulación, la contrastaré con el resto de información con que cuento y te daré una evaluación, que incluirá
                      ordenadamente, de manera corta y por viñetas lo siguiente: aspectos correctos e incorrectos de la especulacción,
                      temas generales que recomiendo repasar para que en el futuro la especulación sea mejor y por ultimo te incluiré
                      el análisis del mercado que considero correcto para el rango de tiempo estudiado.

                      Dame tu especulación: '''

    configIA =[
        {'role': 'user', 'content':tiempo_analizado },
        {'role': 'user', 'content':regresion_lineal },
        {'role': 'user', 'content':pmiUSD_zona },
        {'role': 'user', 'content':pmiEuro_zona },
        {'role': 'user', 'content':ipcEuro_zona },
        {'role': 'system', 'content': personalidad},
        ]

    return configIA

#Función que permite conectarse con openAI en el modo Chat ChatCompletion, recibe el historial = contextoIA(..,..,..,) y texto = nueva entrada
#Retorna una respuesta al estilo CHATGP
def obtener_respuesta(texto, historial):
    respuesta = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=historial + [{'role': 'user', 'content': texto}],
        temperature = 0.2  #Temperatura deterministica/muy coherente al estar lejos de 1
    )
    respuesta_asistente = respuesta['choices'][0]['message']['content']
    return respuesta_asistente

#Main para testeo  -----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    symbol = 'EURUSD=X'
    #Establciendo la API key con la que se logra la conexión con Open AI.
    #Es un parametro único.
    openai.api_key = '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'
    # Obtener fechas
    start_date = input("Ingrese la fecha de inicio (año-mes-día): ")
    end_date = input("Ingrese la fecha de fin (año-mes-día): ")
    # Obtener datos históricos
    data = obtener_datos_historicos(symbol, start_date, end_date)
    # Calcular regresión lineal
    coeficiente, intercepto = calcular_regresion_lineal(data)
    #Visualizando el coeficiente de regresion
    print("regresion : " + str(coeficiente) + "\n" )

    #Setiando un ejemplo de indicadores del mercado
    pmi_eur_prevision = float( 45.5 )
    pmi_eur_actual = float( 45.8 )
    pmi_usd_prevision = float( 50.4 )
    pmi_usd_actual = float( 50.2 )
    ipc_eur_prevision = float(0.9)
    ipc_eur_actual = float(0.7)


    texto_usuario = input("Especulación del trader: ")
    configChatGpt = contextoIA  (start_date,end_date,coeficiente,pmi_usd_prevision,pmi_usd_actual,pmi_eur_prevision,pmi_eur_actual,ipc_eur_prevision,ipc_eur_actual)
    respuesta_asistente = obtener_respuesta(texto_usuario, configChatGpt)

    # Imprime la respuesta del asistente/IA

    print("Asistente:", respuesta_asistente)
