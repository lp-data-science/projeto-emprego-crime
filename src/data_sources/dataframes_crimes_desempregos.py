import glob
import os
import pandas as pd
from os.path import join

CURRENT_DIR = os.getcwd()
CRIMES_DESEMPREGO_DIR = join(CURRENT_DIR, "data_sources/dados_crimes_desemprego/*.csv")
FILES_CRIMES_DESEMPREGO_NAMES = glob.glob(CRIMES_DESEMPREGO_DIR)


def getDesligadosUF():
    global FILES_CRIMES_DESEMPREGO_NAMES
    df_desligados_uf = list(filter(lambda x: x == CURRENT_DIR +
                                    "/data_sources/dados_crimes_desemprego/df_desemprego_group_by_desligados_uf.csv",
                                   FILES_CRIMES_DESEMPREGO_NAMES))
    dataframe = pd.read_csv(df_desligados_uf[0])
    return dataframe


def getOcorrenciasByCrime():
    global FILES_CRIMES_DESEMPREGO_NAMES
    df_ocorrencias_by_crime = list(filter(lambda x: x == CURRENT_DIR +
                                    "/data_sources/dados_crimes_desemprego/df_ocorrencias_group_by_crime.csv",
                                          FILES_CRIMES_DESEMPREGO_NAMES))
    dataframe = pd.read_csv(df_ocorrencias_by_crime[0])
    return dataframe


def getPopulacao():
    global FILES_CRIMES_DESEMPREGO_NAMES
    df_populacao = list(filter(lambda x: x == CURRENT_DIR +
                                    "/data_sources/dados_crimes_desemprego/df_populacao.csv",
                               FILES_CRIMES_DESEMPREGO_NAMES))
    dataframe = pd.read_csv(df_populacao[0])
    return dataframe
