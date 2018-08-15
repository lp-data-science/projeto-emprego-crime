from functools import reduce
from os import getcwd
from os.path import join
import pandas as pd
from ast import literal_eval
import glob


CURRENT_DIR = getcwd()
EMPREGOS_DIR = join(CURRENT_DIR, "data_sources/dados_empregos/*.txt")
CORRELACAO_DIR = join(CURRENT_DIR, "data_sources/dados_empregos/correlacao/*.txt")
FILES_NAMES = glob.glob(EMPREGOS_DIR)
CORRELACAO_FILES_NAMES = glob.glob(CORRELACAO_DIR)

def fillDataFramesEmpregos(file):
    """
    Função que retorna um dataframe gerado a partir dos dados do arquivo lido
    :param file: String
    :return: Dictionary
    """
    data_frame_dict = {}
    f = open(file, 'r', encoding='iso-8859-15')
    line = f.readline()
    dict = literal_eval(line)
    key = dict["nome_estendido"][39:]
    df = pd.DataFrame(dict["valores"])
    data_frame_dict[key] = df
    f.close()

    return data_frame_dict


def getDataFramesEmpregos():
    """
    Função que mapeia a função de geração de dataframes no arquivo
    :return: List
    """
    global FILES_NAMES
    return list(map(fillDataFramesEmpregos, FILES_NAMES))


def dataFrameEmpregosFromJson(filename):
    """
    Função que gera dataframes a partir dos arquivos de uma forma especial para gerar o dataframe do gráfico de
    correlação
    :param filename: String
    :return: pandas.DataFrame
    """
    f = open(filename, 'r', encoding='iso-8859-15')
    line = f.readline()
    dict = literal_eval(line)
    key = dict["nome_estendido"][39:]
    ad = key.split(",")[-1].strip(" ")
    categoria = key.split("-")[0].strip(" ")
    df = pd.DataFrame(dict["valores"])
    df["categoria"] = categoria
    df["admitidos/desligados"] = ad
    f.close()
    return df



def getDataFrameEmpregosFromJson():
    """
    Função que retorna o dataframe com os valores condensados em um só
    :return: pandas.DataFrame
    """
    global FILES_NAMES
    list_df_desemprego = list(map(dataFrameEmpregosFromJson, CORRELACAO_FILES_NAMES))
    df_desemprego = reduce(lambda df1, df2: pd.concat([df1, df2], ignore_index=True, sort=True), list_df_desemprego)
    df_desemprego_group_by_desligados_uf = df_desemprego.groupby(["estado_ibge", "ano", "admitidos/desligados"])[
        "valor"].sum().reset_index(name='total_desempregados')
    df_desemprego_group_by_desligados_uf = df_desemprego_group_by_desligados_uf[
        df_desemprego_group_by_desligados_uf["admitidos/desligados"] == "Desligado"].reset_index()
    del df_desemprego_group_by_desligados_uf['index']
    return df_desemprego_group_by_desligados_uf