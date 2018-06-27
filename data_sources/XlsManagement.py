import pandas as pd

dir="C:\\Users\\vinic\\Desktop\\Projeto\\ProjetoDatascience\\ProjetoDatascience\\Dados população\\PROJECOES_2013_POPULACAO.xls"

def getState(state):
    if len(state)==2:
        return state

def getDataframe(file, state):
    return file.parse(state)

file = pd.ExcelFile(dir)
lista = file.sheet_names
sheets = list(map(getState, lista))
sheets = list(filter(lambda a: a!=None, sheets))

dfs = [getDataframe(file = file,state = x) for x in sheets]

#df = data_frame.parse("RO")



print(dfs)