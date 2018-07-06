from os import getcwd

import geopandas
from dataframes_população import get_dataframe_ano
import gmplot
from os.path import join
import pandas as pd
import glob
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
estados_dir = join(current_dir, "dados_ocorrencias/estados_2010/estados_2010.shx")
municipios_dir = join(current_dir, "dados_ocorrencias/municipios_2010/municipios_2010.shx")
regioes_dir = join(current_dir, "dados_ocorrencias/regioes_2010/regioes_2010.shx")

files = glob.glob(ocorrencias_dir)
data_frame_list = {}
coords = []

df_municipios = pd.read_csv("municipios_br.csv")

def fillDataFramesOcorrencias(file):
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
    global data_frame_list
    global CRIMES
    df_pop = get_dataframe_ano(arquivo[-4:])
    dataframe_ocorrencia = data_frame_list[arquivo]
    dataframe_ocorrencia_municipio_join = dataframe_ocorrencia.join(df_municipios.set_index('Municipio'),
                                                                    on='Município')
    dataframe_ocorrencia_join_populacao = dataframe_ocorrencia_municipio_join.join(df_pop.set_index('Município'),
                                                                                   on='Município').dropna()
    dataframe_agrupado = dataframe_ocorrencia_join_populacao.groupby(
        ['Tipo_Crime', 'Sigla_UF', 'Latitude', 'Longitude', 'População_residente'])[
        'PC-Qtde_Ocorrências'].sum().reset_index(name='total')

    for crime in CRIMES:
        latitudes = dataframe_agrupado[dataframe_agrupado.Tipo_Crime == crime][
            'Latitude'].astype(float)
        longitudes = dataframe_agrupado[dataframe_agrupado.Tipo_Crime == crime][
            'Longitude'].astype(float)

        proporcao_pop_crimes = (dataframe_agrupado['total'] / dataframe_agrupado['População_residente']) * 1000

        plt.scatter(y=latitudes, x=longitudes, alpha=0.5, s=proporcao_pop_crimes, c='r', )

        plt.savefig("graficos_ocorrencias/{}-{}.png".format(crime, arquivo[-4:]))


list(map(fillDataFramesOcorrencias, files))

gdf = geopandas.GeoDataFrame.from_file(municipios_dir)

gdf.plot(figsize=(19.2, 10.8))

list(map(generateHeatMaps, ARQUIVOS))