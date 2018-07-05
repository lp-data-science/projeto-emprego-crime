from os import getcwd

import folium
import gmaps
import gmplot
from folium import plugins
from folium.plugins import HeatMap
from os.path import join
import pandas as pd
from ast import literal_eval
import glob

current_dir = getcwd()
ocorrencias_dir = join(current_dir, "dados_ocorrencias/*.csv")

files = glob.glob(ocorrencias_dir)
data_frame_list = {}
coords = []

#TODO - tirar o for
with open("Capitais - posição.txt", encoding='iso-8859-15') as coord:
    lines = coord.read().splitlines()
    for line in lines:
        data = line.split(',')
        coords.append(data)

df_coord = pd.DataFrame(coords)

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


list(map(fillDataFramesOcorrencias, files))

b = data_frame_list['ocorrenciasmun-brasil2014']
d = b.join(df_municipios.set_index('Municipio'), on='Município')
b = d.groupby(['Tipo_Crime', 'Sigla_UF', 'Latitude', 'Longitude'])['PC-Qtde_Ocorrências'].sum().reset_index(name='total')

gmap = gmplot.GoogleMapPlotter(-8.0349386, -34.935435, 4.5)

latitudes = b[b.Tipo_Crime == 'Roubo seguido de morte (latrocínio)']['Latitude'].astype(float)
longitudes = b[b.Tipo_Crime == 'Roubo seguido de morte (latrocínio)']['Longitude'].astype(float)
peso = b[b.Tipo_Crime == 'Roubo seguido de morte (latrocínio)']['total'].astype(int)

gmap.heatmap(latitudes, longitudes, threshold=50, radius=15)

gmap.draw("ocorrencias_latrocinio_2014.html")
