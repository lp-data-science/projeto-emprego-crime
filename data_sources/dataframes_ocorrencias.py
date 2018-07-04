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
d = b.join(df_coord.set_index(3), on='Sigla_UF')
b = d.groupby(['Tipo_Crime', 'Sigla_UF', 1, 2])['PC-Qtde_Ocorrências'].sum().reset_index(name='total')

# maximo = b[b.Tipo_Crime == 'Estupro']['total'].max()
#
# hmap = folium.Map(location=[-8.0349386, -34.935435], zoom_start=4)
#
# hm_wide = plugins.HeatMap(
#     zip(b[b.Tipo_Crime == 'Estupro'][1].astype(float), b[b.Tipo_Crime == 'Estupro'][2].astype(float), b[b.Tipo_Crime == 'Estupro']['total'].astype(float)),
#     min_opacity=0.2,
#     max_val=maximo,
#     radius=10,
#     blur=15,
#     max_zoom=3,
# )

gmap = gmplot.GoogleMapPlotter(-8.0349386, -34.935435, 4.5)

latitudes = b[b.Tipo_Crime == 'Estupro'][1].astype(float)
longitudes = b[b.Tipo_Crime == 'Estupro'][2].astype(float)
peso = b[b.Tipo_Crime == 'Estupro']['total'].astype(int)

gmap.heatmap(latitudes, longitudes, threshold=50, radius=40)

gmap.draw("my_heatmap.html")
#
#
# hmap.add_child(plugins.HeatMap(zip(latitudes, longitudes, peso), radius=10000))
# hmap.save("teste.html")

fig = gmaps.figure()
heatmap_layer = gmaps.heatmap_layer(
    list(zip(latitudes, longitudes)), weights=peso,
    max_intensity=30, point_radius=3.0
)

fig.add_layer(heatmap_layer)

fig
