import glob
import os
import pandas as pd
from os.path import join

current_dir = os.getcwd()
crimes_desemprego_dir = join(current_dir, "data_sources/dados_crimes_desemprego/*.csv")
arquivos_crimes_desempregos = glob.glob(crimes_desemprego_dir)


def getDesligadosUF():
    global arquivos_crimes_desempregos
    df_desligados_uf = list(filter(lambda x: x == current_dir +
                                    "/data_sources/dados_crimes_desemprego/df_desemprego_group_by_desligados_uf.csv",
                                    arquivos_crimes_desempregos))
    dataframe = pd.read_csv(df_desligados_uf[0])
    return dataframe


def getOcorrenciasByCrime():
    global arquivos_crimes_desempregos
    df_ocorrencias_by_crime = list(filter(lambda x: x == current_dir +
                                    "/data_sources/dados_crimes_desemprego/df_ocorrencias_group_by_crime.csv",
                                    arquivos_crimes_desempregos))
    dataframe = pd.read_csv(df_ocorrencias_by_crime[0])
    return dataframe


def getPopulacao():
    global arquivos_crimes_desempregos
    df_populacao = list(filter(lambda x: x == current_dir +
                                    "/data_sources/dados_crimes_desemprego/df_populacao.csv",
                                    arquivos_crimes_desempregos))
    dataframe = pd.read_csv(df_populacao[0])
    return dataframe
