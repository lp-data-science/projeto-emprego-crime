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

    f = open(file, 'r', encoding='iso-8859-15')

    df = pd.read_csv(f, sep=';')

    file_list = file.split('/')

    file_name = file_list[7][0:-4]



    data_frame_list[file_name] = df

    f.close()

    return data_frame_list
