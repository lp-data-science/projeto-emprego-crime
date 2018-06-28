from os import getcwd
from os.path import join
import pandas as pd
from ast import literal_eval
import glob

current_dir = getcwd()
empregos_dir = join(current_dir, "dados_empregos/*.txt")
file_name = 'Número de Admitidos-Desligados por UF, Faixa Etária até 17 Anos - Admitidos-Desligados, Ad.txt'

dataframe_list = {}

#file = open(join(empregos_dir, file_name), 'r', encoding='iso-8859-15')

files=glob.glob(empregos_dir)
for file in files:
    f = open(file, 'r', encoding='iso-8859-15')
    line = f.readline()
    dict = literal_eval(line)
    key = dict["nome"]

    df = pd.DataFrame(dict["valores"])
    dataframe_list[key] = df


    f.close()

for key in dataframe_list:
    print(key)
    print(dataframe_list[key])
