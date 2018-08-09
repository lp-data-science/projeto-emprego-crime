import glob
from functools import reduce
import os
import pandas as pd
from os.path import join
from src.utils.utils import REGIOES, ESTADOS_SIGLAS

CURRENT_DIR = os.getcwd()
PLANILHA_POPULACAO = join(CURRENT_DIR, "data_sources/dados_populacao/PROJECOES_2013_POPULACAO.xls")
DIR_CSV_POPULACAO = join(CURRENT_DIR, "data_sources/dados_populacao/*.csv")

FILES_NAMES = glob.glob(DIR_CSV_POPULACAO)


def createDataframes(ano):
    dir_csv = join(CURRENT_DIR, 'data_sources/dados_populacao/estados_pop_{}.csv'.format(ano))
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


# def plotEstado(estado,cor):
#
#     df = (dic_state_population[estado]["state"])
#     df = df.iloc[0][11:16]
#     patch = mpatches.Patch(color=cor, label=estado)
#     df.plot(color=cor)
#     return patch


def getRegion(region):
    if region in REGIOES:
        return region


def getDataframeRegions():
    return dfs_regioes


def getDataFramePopulacaoFromCsv():
    global FILES_NAMES
    list_df_populacao = list(map(dataFramePopulacaoFromCsv, FILES_NAMES))
    df_populacao = reduce(lambda df1, df2: pd.concat([df1, df2], ignore_index=True, sort=True), list_df_populacao)
    return df_populacao


def dataFramePopulacaoFromCsv(filename):
    df_estados = pd.DataFrame({"UF": list(ESTADOS_SIGLAS.values()), "Sigla_UF": list(ESTADOS_SIGLAS.keys())})
    ano = filename[-8:-4]
    df = pd.read_csv(filename, encoding="utf-8", sep=',')
    df["ano"] = ano
    new_df = pd.merge(df, df_estados, on=['Sigla_UF'], how="left")
    return new_df


file = pd.ExcelFile(PLANILHA_POPULACAO)
lista = file.sheet_names
sheets = list(map(getState, lista))
sheets = list(filter(lambda a: a != None, sheets))

region_list = list(map(getRegion, lista))
region_list = list(filter(lambda a: a != None, region_list))

# dfs = [getDataframe(file=file, state=x) for x in sheets]
#
dfs_regioes = [getDataframe(file=file, state=region) for region in region_list]

# dic_state_population = {}
#
# for i in sheets:
#     dic_state_population[i] = {}

