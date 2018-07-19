from os import getcwd
from os.path import join
import pandas as pd
from ast import literal_eval
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

current_dir = getcwd()
empregos_dir = join(current_dir, "data_sources/dados_empregos/*.txt")

files_names = glob.glob(empregos_dir)
data_frame_dict = {}

result_keyIBGE = []
result_keySexo = []

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
    global result_keyIBGE
    global  result_keySexo
    key, value = dictElement

    if key[0:10] == 'Setor IBGE' and key[-10:] == ' Desligado':
         result_keyIBGE.append(key)
    elif key[0:4] == 'Sexo' and key[-10:] == ' Desligado':
        result_keySexo.append(key)







handlesIBGE = []
colorsIBGE = ['mediumblue', 'red', 'lime', 'purple', 'grey', 'black', 'darkolivegreen']
axIBGE = None

def plotByKeySetorIBGE(key):
    global data_frames
    global axIBGE
    global handlesIBGE
    global colorsIBGE

    data_frame = data_frames[key]
    setor = key[11:].split('-')
    setor = setor[0]
    data_frame = data_frame[data_frame.estado_ibge == 26]
    color = colorsIBGE.pop(0)
    if axIBGE == None:

        axIBGE = data_frame.plot(color=color, x='ano', y='valor')
    else:
        axIBGE = data_frame.plot(color=color, x='ano', y='valor', ax=axIBGE)

    patch = mpatches.Patch(color=color, label=setor)
    handlesIBGE.append(patch)


listDataframeSexo = []

def getDataframesBySexo(key):
    global data_frames
    global axSexo
    global handlesSexo
    global colorsSexo

    data_frame = data_frames[key]
    listDataframeSexo.append(data_frame)


def plotDesempregoGeral():
    data_frame1 = listDataframeSexo[0]
    data_frame2 = listDataframeSexo[1]

    geral = pd.DataFrame({'ano': data_frame1.ano, 'estado_ibge': data_frame1.estado_ibge,
                          'valor': data_frame1.valor + data_frame2.valor})
    data_frame = geral[geral.estado_ibge == 26]

    data_frame.plot(color='red', x='ano', y='valor')



list(map(getKey, data_frames.items()))
list(map(getDataframesBySexo, result_keySexo))
plotDesempregoGeral()

list(map(plotByKeySetorIBGE, result_keyIBGE))








plt.legend(title='Setor', handles=handlesIBGE)
plt.xlabel("ano")
plt.ylabel("população")
plt.show()