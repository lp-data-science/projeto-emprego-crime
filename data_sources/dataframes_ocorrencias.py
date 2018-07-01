from os import getcwd
from os.path import join
import pandas as pd
from ast import literal_eval
import glob

current_dir = getcwd()
ocorrencias_dir = join(current_dir, "dados_ocorrencias/*.csv")

files = glob.glob(ocorrencias_dir)
data_frame_list = {}

def fillDataFramesOcorrencias(file):
    global data_frame_list

    f = open(file, 'r', encoding='utf-8')

    df = pd.read_csv(f, sep=';')

    file_list = file.split('/')

    file_name = file_list[7][0:-4]

    data_frame_list[file_name] = df

    f.close()

    return data_frame_list

for file in files:
    a = fillDataFramesOcorrencias(file)
b = data_frame_list['ocorrenciasmun-brasil2014'].where(data_frame_list['ocorrenciasmun-brasil2014']['Tipo Crime'] == 'Estupro')
c = b.where(b['Sigla UF'] == 'PB')
print(b['Tipo Crime'].dropna())
print(b['PC-Qtde Ocorrências'].dropna())
print(c.dropna())