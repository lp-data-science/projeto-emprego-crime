from os import getcwd
from os.path import join
import pandas as pd
from ast import literal_eval
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

CURRENT_DIR = getcwd()
EMPREGOS_DIR = join(CURRENT_DIR, "data_sources/dados_empregos/*.txt")

FILES_NAMES = glob.glob(EMPREGOS_DIR)


def fillDataFramesEmpregos(file):
    data_frame_dict = {}
    f = open(file, 'r', encoding='iso-8859-15')
    line = f.readline()
    dict = literal_eval(line)
    key = dict["nome_estendido"][39:]
    df = pd.DataFrame(dict["valores"])
    data_frame_dict[key] = df
    f.close()

    return data_frame_dict


def getDataFramesEmpregos():
    global FILES_NAMES
    return list(map(fillDataFramesEmpregos, FILES_NAMES))
