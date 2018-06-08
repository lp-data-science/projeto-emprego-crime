import requests
import matplotlib.pyplot as pl
import pandas as pd


def createDF(dicionario):
    dataf = pd.DataFrame(lista_dicionarios)
    return dataf


def concatDF(df1, df2):
    return pd.concat([df1, df2], ignore_index=True)


r = requests.get('http://206.81.2.122/empregos/v1/crimes/1')

res_json = r.json()

lista_dicionarios = res_json['message']

dataframe = createDF(lista_dicionarios)

dataframe_mes = dataframe[dataframe.data == "2010-09-01T00:00:00.000Z"]

pl.bar(dataframe_mes["data"], dataframe_mes["quantidade"])

pl.show()
