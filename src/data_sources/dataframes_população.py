import glob
from os import getcwd
import pandas as pd
from os import getcwd
from os.path import join
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from src.utils.utils import ANOS, REGIOES

dataframes_population = {} # Todos os dataframes

current_dir = getcwd()
dir = join(current_dir, "data_sources/dados_populacao/PROJECOES_2013_POPULACAO.xls")
state_pop_files = join(current_dir, "data_sources/dados_populacao/*.csv")

pop_csv = glob.glob(state_pop_files)

def createDataframes(ano):
    dir_csv = join(current_dir, 'data_sources/dados_populacao/estados_pop_{}.csv'.format(ano))
    df = pd.read_csv(dir_csv, encoding='utf-8', sep=',')
    df_size = len(df)
    df.loc[:, 'ano'] = pd.Series([int(ano)] * df_size)
    df = df.rename(columns={'CD_GEOCUF': 'estado_ibge'})
    return df


def getDataframePopState(ano):
    return createDataframes(ano)

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


def plotEstado(estado,cor):

    df = (dic_state_population[estado]["state"])
    df = df.iloc[0][11:16]
    patch = mpatches.Patch(color=cor, label=estado)
    df.plot(color=cor)
    return patch

def getRegion(region):
    if region in REGIOES:
        return region

file = pd.ExcelFile(dir)
lista = file.sheet_names
sheets = list(map(getState, lista))
sheets = list(filter(lambda a: a != None, sheets))

region_list = list(map(getRegion, lista))
region_list = list(filter(lambda a: a != None, region_list))

dfs = [getDataframe(file=file, state=x) for x in sheets]

dfs_regioes = [getDataframe(file=file, state=region) for region in region_list]

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


def getDataframeRegions():
    return dfs_regioes

# handles = []
#
# handles.append(plotEstado('PE','blue'))
# handles.append(plotEstado('PB', 'red'))
# handles.append(plotEstado('BA','pink'))
# handles.append(plotEstado('AL', 'grey'))
# handles.append(plotEstado('SE', 'green'))
# handles.append(plotEstado('PI', 'yellow'))
# handles.append(plotEstado('MA', 'magenta'))
# handles.append(plotEstado('CE','lime'))
#
# plt.legend(title='Estados', handles=handles)
#
# plt.xlabel("ano")
# plt.ylabel("população")
# plt.savefig("populacao_ano.png")
# plt.show()
