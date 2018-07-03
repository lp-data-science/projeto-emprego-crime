from os import getcwd
import folium
import gmplot
from folium import plugins
from folium.plugins import HeatMap
from os.path import join
import pandas as pd
import geopandas as gpd

current_dir = getcwd()
dir = join(current_dir, 'dados_populacao/PROJECOES_2013_POPULACAO.xls')


def getState(state):
    if len(state)==2:
        return state

def getDataframe(file, state):
    return file.parse(state)


def getMenPopulation(data_frame):
    return data_frame.iloc[3:24]


def getWomenPopulation(data_frame):
    return data_frame.iloc[26:47]


def getStatePopulation(data_frame):
    return data_frame.iloc[49:70]


file = pd.ExcelFile(dir)
lista = file.sheet_names
sheets = list(map(getState, lista))
sheets = list(filter(lambda a: a!=None, sheets))

dfs = [getDataframe(file = file,state = x) for x in sheets]

data_frame_population_men= list(map(getMenPopulation, dfs))
data_frame_population_women = list(map(getWomenPopulation, dfs))
data_frame_population_state = list(map(getStatePopulation, dfs))

dic_state_population={}
for i in sheets:
    dic_state_population[i]={}

for i in range(0,len(sheets)):
    dic_state_population[sheets[i]]["men"]=data_frame_population_men[i]
    dic_state_population[sheets[i]]["women"]=data_frame_population_women[i]
    dic_state_population[sheets[i]]["state"]=data_frame_population_state[i]


"""
TESTES
"""
print(type(dic_state_population['PE']['state']))
print(type(dic_state_population['PE']))

dic_state_population['PE']['state'].insert(0, 'LAT', -8.0349386)
dic_state_population['PE']['state'].insert(0, 'LON', -34.935435)

max_amount = float(dic_state_population['PE']['state']['Unnamed: 1'].max())
hmap = folium.Map(location=[-8.0349386, -34.935435], zoom_start=7)
hm_wide = HeatMap(
    zip(dic_state_population['PE']['state']['LAT'], dic_state_population['PE']['state']['LON'], dic_state_population['PE']['state']['Unnamed: 1']),
    min_opacity=0.2,
    max_val=max_amount,
    radius=17,
    blur=15,
    max_zoom=1,
)

gmap = gmplot.GoogleMapPlotter(-8.0349386, -34.935435, 7)
latitudes = dic_state_population['PE']['state']['LAT']
longitudes = dic_state_population['PE']['state']['LON']
gmap.heatmap(latitudes, longitudes)
gmap.draw("my_heatmap.html")

hmap.add_child(hm_wide)
print(max_amount)
hmap.save("teste.html")
#print(dic_state_population['PE']['state']['Unnamed: 1'])