from os import getcwd

import geopandas
from dataframes_população import get_dataframe_ano
import gmplot
from os.path import join
import pandas as pd
import glob
import matplotlib.pyplot as plt

plt.style.use('bmh')

current_dir = getcwd()
ocorrencias_dir = join(current_dir, "dados_ocorrencias/*.csv")
estados_dir = join(current_dir, "dados_ocorrencias/estados_2010/estados_2010.shx")
municipios_dir = join(current_dir, "dados_ocorrencias/municipios_2010/municipios_2010.shx")

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

df_pop = get_dataframe_ano('2014')

list(map(fillDataFramesOcorrencias, files))

gdf = geopandas.GeoDataFrame.from_file(municipios_dir)

gdf.plot()



dataframe_ocorrencia = data_frame_list['ocorrenciasmun-brasil2014']
dataframe_ocorrencia_municipio_join = dataframe_ocorrencia.join(df_municipios.set_index('Municipio'), on='Município')
dataframe_ocorrencia_join_populacao = dataframe_ocorrencia_municipio_join.join(df_pop.set_index('Município'), on='Município').dropna()
dataframe_agrupado = dataframe_ocorrencia_join_populacao.groupby(['Tipo_Crime', 'Sigla_UF', 'Latitude', 'Longitude'])['PC-Qtde_Ocorrências'].sum().reset_index(name='total')
#
# gmap = gmplot.GoogleMapPlotter(-8.0349386, -34.935435, 4.5)
#
latitudes = dataframe_agrupado[dataframe_agrupado.Tipo_Crime == 'Roubo seguido de morte (latrocínio)']['Latitude'].astype(float)
longitudes = dataframe_agrupado[dataframe_agrupado.Tipo_Crime == 'Roubo seguido de morte (latrocínio)']['Longitude'].astype(float)

plt.scatter(y=latitudes, x=longitudes, alpha=0.5, c='r')

plt.show()
# quantidade = dataframe_agrupado[dataframe_agrupado.Tipo_Crime == 'Roubo seguido de morte (latrocínio)']['total'].astype(int)
# populacao = dataframe_ocorrencia_join_populacao[dataframe_ocorrencia_join_populacao.Tipo_Crime == 'Roubo seguido de morte (latrocínio)']['População_residente'].astype(int)
#
# gmap.heatmap(latitudes, longitudes, threshold=50, radius=15)
#
# gmap.draw("ocorrencias_latrocinio_teste.html")
