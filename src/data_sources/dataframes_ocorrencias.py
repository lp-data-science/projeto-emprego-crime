from functools import reduce
from os import getcwd
from os.path import join
from src.data_sources.dataframes_população import getDataframePopState
from src.utils.utils import ARQUIVOS_OCORRENCIAS, CRIMES, ANOS
import glob
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

plt.style.use('bmh')


CURRENT_DIR = getcwd()
OCORRENCIAS_DIR = join(CURRENT_DIR, "data_sources/dados_ocorrencias/*.csv")
ESTADOS_DIR = join(CURRENT_DIR, "data_sources/dados_ocorrencias/estados_shp/BRUFE250GC_SIR.shp")
FILES_NAMES = glob.glob(OCORRENCIAS_DIR)


def getDataframesOcorrenciasAno(ano):
    """
    função que retorna o dataframe das ocorrências de um ano específico
    :param ano: int
    :return: dataframe
    """

    global FILES_NAMES
    global ESTADOS_DIR

    df_pop = getDataframePopState(ano)
    file = list(filter(lambda x: x[-8:-4] == str(ano), FILES_NAMES))

    # file[0] = file[0].split('/')

    file_csv = file[0][-3] + '/' + file[0][-2] + '/' + file[0][-1]

    f = open(file[0], 'r', encoding='utf-8')
    df = pd.read_csv(f, sep=';')
    df_crime_cod_uf = df.join(df_pop.set_index("Sigla_UF"), on="Sigla_UF").dropna()
    f.close()

    return df_crime_cod_uf


def getDataframesTotalOcorrencias():
    df = list(map(getDataframesOcorrenciasAno, ANOS))
    df_conc = pd.concat(df, ignore_index=True, sort=True)
    return df_conc


def getDataframesOcorrenciasCrime(crime, ano):
    """
    função que retorna dados de um crime específico de um determinado ano
    :param crime: string
    :param ano: int
    :return: dataframe
    """
    global ESTADOS_DIR

    df_year = getDataframesOcorrenciasAno(ano)
    df_crime = df_year.loc[df_year["Tipo_Crime"] == crime]

    return df_crime


def getDataframesOcorrenciasEstado(UF, ano):
    """
    função que retorna dados de um estado específico em um determinado ano
    :param UF: string
    :param ano: int
    :return: dataframe
    """
    df_year = getDataframesOcorrenciasAno(ano)
    df_estado = df_year.loc[df_year["Sigla_UF"] == UF]
    return df_estado


def plotEstadoHeatMap(arquivo,df_groupby, crime):

    global estados_dir

    brazil_shape = gpd.read_file(estados_dir)
    df_brazil_shape = pd.DataFrame(brazil_shape)
    df_brazil_shape["CD_GEOCUF"] = df_brazil_shape["CD_GEOCUF"].apply(int)

    df_join_groupby_shape = df_groupby.join(df_brazil_shape.set_index("CD_GEOCUF"),
                                            on="CD_GEOCUF")

    df_join_groupby_shape["proporcao"] = (df_join_groupby_shape.total / df_join_groupby_shape.populacao) * 1000

    geodf_join_groupby_shape = gpd.GeoDataFrame(df_join_groupby_shape[df_join_groupby_shape.Tipo_Crime == crime])

    geodf_join_groupby_shape.plot(column="proporcao", cmap="YlGnBu", legend=True)
    plt.title("Proporcao Crimes X Populacao")
    plt.savefig("data_sources/ocorrencias/fig_{}_{}".format(crime, arquivo[-4:]))


def getDataFrameOcorrenciasFromCsv():
    global FILES_NAMES
    list_df_ocorrencias = list(map(dataFrameOcorrenciasFromCsv, FILES_NAMES))
    df_ocorrencias = reduce(lambda df1, df2: pd.concat([df1, df2], ignore_index=True, sort=True), list_df_ocorrencias)
    df_ocorrencias['ano'] = df_ocorrencias.Mês_Ano.str[3:]
    df_ocorrencias_group_by_crime_ano = df_ocorrencias.groupby(["Tipo_Crime", "UF", "ano"])[
        'PC-Qtde_Ocorrências'].sum().reset_index(name='ocorrencias')
    return df_ocorrencias_group_by_crime_ano


def dataFrameOcorrenciasFromCsv(filename):
    df = pd.read_csv(filename, encoding="utf-8", sep=';')
    return df
