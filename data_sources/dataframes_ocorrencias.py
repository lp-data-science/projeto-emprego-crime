from os import getcwd
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

# print(coords)
df_coord = pd.DataFrame(coords)
# print(df_coord)

def fillDataFramesOcorrencias(file):
    global data_frame_list

    f = open(file, 'r', encoding='utf-8')

    df = pd.read_csv(f, sep=';')

    file_list = file.split('/')
    file_name = file_list[7][0:-4]
    data_frame_list[file_name] = df

    f.close()

    return data_frame_list

#TODO - tirar o for
for file in files:
    a = fillDataFramesOcorrencias(file)
# b = data_frame_list['ocorrenciasmun-brasil2014'].where(data_frame_list['ocorrenciasmun-brasil2014']['Tipo Crime'] == 'Estupro')
# c = b.where(b['Sigla UF'] == 'PB')
# print(b['Tipo Crime'].dropna())
# print(b['PC-Qtde Ocorrências'].dropna())
# print(c.dropna())
b = data_frame_list['ocorrenciasmun-brasil2014']
d = b.join(df_coord.set_index(3), on='Sigla UF')
#print(d)
# b = data_frame_list['ocorrenciasmun-brasil2014'].groupby(['Tipo Crime', 'Sigla UF'])['PC-Qtde Ocorrências'].sum()
b = d.groupby(['Tipo Crime', 'Sigla UF', 1, 2])['PC-Qtde Ocorrências'].sum()
#crimes_estados = b.loc[:,:].index.values
#print(b[b.index.values == ('Estupro','AL')])
print(b)



