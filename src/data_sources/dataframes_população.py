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
    """
    Função que cria os dataframes a partir dos arquivos csv
    :param ano: String
    :return: pandas.DataFrame
    """
    dir_csv = join(CURRENT_DIR, 'data_sources/dados_populacao/estados_pop_{}.csv'.format(ano))
    df = pd.read_csv(dir_csv, encoding='utf-8', sep=',')
    df_size = len(df)
    df.loc[:, 'ano'] = pd.Series([int(ano)] * df_size)
    df = df.rename(columns={'CD_GEOCUF': 'estado_ibge'})
    return df


def getDataframePopState(ano):
    """
    Função que possibilita o map para retornar os dataframes
    :param ano: String
    :return: pandas.DataFrame
    """
    return createDataframes(ano)


def getState(state):
    """
    Função que filtra as siglas UF
    :param state: String
    :return: String
    """
    if len(state) == 2:
        return state


def getDataframe(file, state):
    """
    Função que coleta os dados da base na UF especificada
    :param file: String
    :param state: String
    :return: pandas.DataFrame
    """
    return file.parse(state)


def getStatePopulation(data_frame):
    """
    Função que coleta as colunas e linhas referentes ao total de população
    :param data_frame: pandas.DataFrame
    :return: pandas.DataFrame
    """
    data_frame.columns = (data_frame.iloc[49]).tolist()
    return data_frame.iloc[50:70]


def getRegion(region):
    """
    Função que retorna a região
    :param region: String
    :return: String
    """
    if region in REGIOES:
        return region


def getDataframeRegions():
    """
    Função que retorna os dataframes das regiões com a respectiva população
    :return: pandas.DataFrame
    """
    dfs_regioes = [getDataframe(file=SHEET_FILE, state=region) for region in REGION_LIST]
    return dfs_regioes


def getDataFramePopulacaoFromCsv():
    """
    Função que retorna os dataframes de população condensado em um, a fim de gerar o dataframe utilizado para calcular
    a correlação
    :return: pandas.DataFrame
    """
    global FILES_NAMES
    list_df_populacao = list(map(dataFramePopulacaoFromCsv, FILES_NAMES))
    df_populacao = reduce(lambda df1, df2: pd.concat([df1, df2], ignore_index=True, sort=True), list_df_populacao)
    return df_populacao


def dataFramePopulacaoFromCsv(filename):
    """
    Função que cria os dataframes de população a partir do csv, a fim de gerar o dataframe utilizado para
    calcular a correlação.
    :param filename: String
    :return: pandas.DataFrame
    """
    df_estados = pd.DataFrame({"UF": list(ESTADOS_SIGLAS.values()), "Sigla_UF": list(ESTADOS_SIGLAS.keys())})
    ano = filename[-8:-4]
    df = pd.read_csv(filename, encoding="utf-8", sep=',')
    df["ano"] = ano
    new_df = pd.merge(df, df_estados, on=['Sigla_UF'], how="left")
    return new_df


SHEET_FILE = pd.ExcelFile(PLANILHA_POPULACAO)
SHEETS_LIST = SHEET_FILE.sheet_names
SHEETS = list(map(getState, SHEETS_LIST))
SHEETS = list(filter(lambda a: a != None, SHEETS))

REGION_LIST = list(map(getRegion, SHEETS_LIST))
REGION_LIST = list(filter(lambda a: a != None, REGION_LIST))