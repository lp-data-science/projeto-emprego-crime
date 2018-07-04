from os import getcwd

from data_sources.dataframes_ocorrencias import crimeByAno

'''import folium
import gmplot
from folium import plugins
from folium.plugins import HeatMap'''
from os.path import join
import pandas as pd
# import geopandas as gpd
from os import getcwd
from os.path import join
from dataframes_ocorrencias import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


current_dir = getcwd()
dir = join(current_dir, "dados_populacao/PROJECOES_2013_POPULACAO.xls")

current_dir = getcwd()
dir = join(current_dir, 'dados_populacao/PROJECOES_2013_POPULACAO.xls')


def getState(state):
    if len(state) == 2:
        return state


def getDataframe(file, state):
    return file.parse(state)


def getMenPopulation(data_frame):
    data_frame.columns = (data_frame.iloc[3]).tolist()
    return data_frame.iloc[4:24]


def getWomenPopulation(data_frame):
    data_frame.columns = (data_frame.iloc[26]).tolist()
    return data_frame.iloc[27:47]


def getStatePopulation(data_frame):

    data_frame.columns = (data_frame.iloc[49]).tolist()
    return data_frame.iloc[50:70]


file = pd.ExcelFile(dir)
lista = file.sheet_names
sheets = list(map(getState, lista))
sheets = list(filter(lambda a: a != None, sheets))

dfs = [getDataframe(file=file, state=x) for x in sheets]


data_frame_population_men = list(map(getMenPopulation, dfs))
data_frame_population_women = list(map(getWomenPopulation, dfs))
data_frame_population_state = list(map(getStatePopulation, dfs))

dic_state_population = {}
for i in sheets:
    dic_state_population[i] = {}

for i in range(0, len(sheets)):
    dic_state_population[sheets[i]]["men"] = data_frame_population_men[i]
    dic_state_population[sheets[i]]["women"] = data_frame_population_women[i]
    dic_state_population[sheets[i]]["state"] = data_frame_population_state[i]



df = (dic_state_population["PE"]["state"])
df = df.iloc[0][11:16]
blue_patch = mpatches.Patch(color='blue', label='PE')
df.plot(color='blue')

df2 = (dic_state_population["SP"]["state"])
df2 = df2.iloc[0][11:16]
red_patch = mpatches.Patch(color='red', label='SP')
plt.legend(title='Estados', handles=[red_patch, blue_patch])
df2.plot(color='red')


plt.xlabel("ano")
plt.ylabel("população")
plt.show()
