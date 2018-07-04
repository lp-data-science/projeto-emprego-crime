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


def createMap(tupla_crime_uf):
    """
    função para retornar os valores totais dos crimes por cada chave
    """
    global b
    return b[tupla_crime_uf]


#TODO - tirar o for
for file in files:
    a = fillDataFramesOcorrencias(file)

def crimeByAno (crime,ano):
    b = data_frame_list['ocorrenciasmun-brasil%s'%(ano)]
    d = b.join(df_coord.set_index(3), on='Sigla_UF')
    b = d.groupby(['Tipo_Crime', 'Sigla_UF', 1, 2])['PC-Qtde_Ocorrências'].sum().reset_index(name='total')

    return(b[b.Tipo_Crime == crime])




