import pandas as pd
from os import getcwd
from os.path import join

current_dir = getcwd()
dir = join(current_dir, "dados_populacao/PROJECOES_2013_POPULACAO.xls")


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
#df = data_frame.parse("RO")

dic_state_population={}
for i in sheets:
    dic_state_population[i]={}

for i in range(0,len(sheets)):
    dic_state_population[sheets[i]]["men"]=data_frame_population_men[i]
    dic_state_population[sheets[i]]["women"]=data_frame_population_women[i]
    dic_state_population[sheets[i]]["state"]=data_frame_population_state[i]
    
print(dic_state_population)