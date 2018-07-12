from os import getcwd
from os.path import join
from dataframes_população import getDataframePopState
import glob
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

plt.style.use('bmh')

CRIMES = [
    'Roubo seguido de morte (latrocínio)',
    'Roubo de veículo',
    'Lesão corporal seguida de morte',
    'Homicídio doloso',
    'Furto de veículo',
    'Estupro'
]

ANOS = [
    '2010',
    '2011',
    '2012',
    '2013',
    '2014'
]

ARQUIVOS = [
    'ocorrenciasmun-brasil2010',
    'ocorrenciasmun-brasil2011',
    'ocorrenciasmun-brasil2012',
    'ocorrenciasmun-brasil2013',
    'ocorrenciasmun-brasil2014'
]

current_dir = getcwd()
ocorrencias_dir = join(current_dir, "dados_ocorrencias/*.csv")
estados_dir = join(current_dir, "dados_ocorrencias/estados_shp/BRUFE250GC_SIR.shp")
files = glob.glob(ocorrencias_dir)
data_frame_list = {}
coords = []


def fillDataframesOcorrencias(file):
    global data_frame_list

    f = open(file, 'r', encoding='utf-8')

    df = pd.read_csv(f, sep=';')

    file_list = file.split('/')
    file_name = file_list[7][0:-4]
    data_frame_list[file_name] = df

    f.close()

    return data_frame_list


def createMap(tupla_crime_uf):
    """
    função para retornar os valores totais dos crimes por cada chave
    """
    global b
    return b[tupla_crime_uf]


def generateHeatMaps(arquivo):
    """
    função que plota os gráficos dos crimes entre os anos
    :param arquivo: Dados de ocorrências
    :return: void
    """
    global data_frame_list
    global CRIMES
    global estados_dir

    df_pop = getDataframePopState(arquivo[-4:])

    df_ocorrencia = data_frame_list[arquivo]

    df_ocorrencia_populacao = df_ocorrencia.join(df_pop.set_index("UF"), on="Sigla_UF").dropna()

    df_groupby = df_ocorrencia_populacao.groupby(
        ['Tipo_Crime', 'Sigla_UF', 'CD_GEOCUF', 'populacao'])[
        'PC-Qtde_Ocorrências'].sum().reset_index(name='total')

    for crime in CRIMES:
        brazil_shape = gpd.read_file(estados_dir)
        df_brazil_shape = pd.DataFrame(brazil_shape)
        df_brazil_shape["CD_GEOCUF"] = df_brazil_shape["CD_GEOCUF"].apply(int)

        df_join_groupby_shape = df_groupby.join(df_brazil_shape.set_index("CD_GEOCUF"),
                                                on="CD_GEOCUF")

        df_join_groupby_shape["proporcao"] = (df_join_groupby_shape.total / df_join_groupby_shape.populacao) * 1000

        geodf_join_groupby_shape = gpd.GeoDataFrame(df_join_groupby_shape[df_join_groupby_shape.Tipo_Crime == crime])

        geodf_join_groupby_shape.plot(column="proporcao", cmap="YlGnBu", legend=True)
        plt.title("Proporcao Crimes X Populacao")
        plt.savefig("graficos_ocorrencias/fig_{}_{}".format(crime, arquivo[-4:]))


list(map(fillDataframesOcorrencias, files))
list(map(generateHeatMaps, ARQUIVOS))