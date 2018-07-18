from os import getcwd
from os.path import join
import pandas as pd
from ast import literal_eval
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

current_dir = getcwd()
empregos_dir = join(current_dir, "dados_empregos/*.txt")

files_names = glob.glob(empregos_dir)
data_frame_dict = {}

result_key = []

def fillDataFramesEmpregos(file):
    global data_frame_dict
    global file_names

    f = open(file, 'r', encoding='iso-8859-15')
    line = f.readline()
    dict = literal_eval(line)
    key = dict["nome_estendido"][39:]

    df = pd.DataFrame(dict["valores"])
    data_frame_dict[key] = df

    f.close()



def getDataFramesEmpregos():
    global files_names
    global data_frame_dict
    list(map(fillDataFramesEmpregos, files_names))
    return data_frame_dict



data_frames = getDataFramesEmpregos()


def getKey(dictElement):
    global result_key
    key, value = dictElement

    if key[0:10] == 'Setor IBGE' and key[-10:] == ' Desligado':
         result_key.append(key)

handles = []
colors = ['mediumblue', 'red', 'lime', 'purple', 'grey', 'black', 'darkolivegreen']
ax = None

def plotByKey(key):
    global data_frames
    global ax
    global handles
    global colors

    data_frame = data_frames[key]
    setor = key[11:].split('-')
    setor = setor[0]
    data_frame = data_frame[data_frame.estado_ibge == 26]
    color = colors.pop(0)
    if ax == None:
        ax = data_frame.plot(color=color, x='ano', y='valor')
    else:
        ax = data_frame.plot(color=color, x='ano', y='valor', ax=ax)

    patch = mpatches.Patch(color=color, label=setor)
    handles.append(patch)


list(map(getKey, data_frames.items()))

list(map(plotByKey, result_key))

plt.legend(title='Setor', handles=handles)
plt.xlabel("ano")
plt.ylabel("população")
plt.show()