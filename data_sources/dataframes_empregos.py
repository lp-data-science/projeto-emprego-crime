from os import getcwd
from os.path import join
import pandas as pd
from ast import literal_eval
import glob

current_dir = getcwd()
empregos_dir = join(current_dir, "dados_empregos/*.txt")

files = glob.glob(empregos_dir)
data_frame_list = {}

def fillDataFramesEmpregos(file):
    global data_frame_list

    f = open(file, 'r', encoding='iso-8859-15')
    line = f.readline()
    dict = literal_eval(line)
    key = dict["nome"]

    df = pd.DataFrame(dict["valores"])
    data_frame_list[key] = df

    f.close()

    return data_frame_list


def testeDf(key, dataframe_list):
    print(key)
    print(dataframe_list[key])


def getDataFramesEmpregos():
    return list(map(fillDataFramesEmpregos, files))

a = getDataFramesEmpregos()

print(len(a))