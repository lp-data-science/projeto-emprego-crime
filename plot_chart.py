import requests
import matplotlib.pyplot as pl
import pandas as pd


def createDF(dicionario):
    dataf = pd.DataFrame(lista_dicionarios)
    return dataf


r = requests.get('http://206.81.2.122/empregos/v1/crimes/1')

res_json = r.json()

lista_dicionarios = res_json['message']

dataframe = createDF(lista_dicionarios)

fig, ax = pl.subplots(figsize=(15, 7))

dataframe_processed = dataframe.groupby(["data", "tipo_crime"]).count()['quantidade'].unstack().plot(ax=ax)

print(dataframe.groupby(["data", "tipo_crime"]).mean())

pl.show()