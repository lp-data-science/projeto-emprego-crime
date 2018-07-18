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



def fillDataFramesEmpregos(file):
    global data_frame_dict
    global file_names

    f = open(file, 'r', encoding='iso-8859-15')
    line = f.readline()
    dict = literal_eval(line)
    key = dict["nome"]


    df = pd.DataFrame(dict["valores"])
    data_frame_dict[key] = df

    f.close()


def getDataFramesEmpregos():
    global files_names
    global data_frame_dict
    list(map(fillDataFramesEmpregos, files_names))
    return data_frame_dict



# data_frames = getDataFramesEmpregos()


# desempregados_medio_completo = data_frames['Número de Admitidos/Desligados por UF, Grau Instrução, Médio Completo - Admitidos/Desligad']
# desempregados_nono_ano = data_frames['Número de Admitidos/Desligados por UF, Grau Instrução, 6ª a 9ª Fundamental - Admitidos/Des']
#
# '''Build Gráfico'''
# medio_pe = desempregados_medio_completo[desempregados_medio_completo.estado_ibge == 26]
# medio_pe = medio_pe[['ano', 'valor']]
# ax = medio_pe.plot(color='blue', x='ano', y='valor')
# blue_patch = mpatches.Patch(color='blue', label='Ensino médio completo')
#
# nono_pe = desempregados_nono_ano[desempregados_medio_completo.estado_ibge == 26]
# nono_pe = nono_pe[['ano', 'valor']]
# nono_pe.plot(color = 'red', x ='ano', y = 'valor', ax = ax)
# red_patch = mpatches.Patch(color='red', label='5 ao 9 ano')
# plt.legend(title='Estados', handles=[red_patch, blue_patch])
#
# plt.xlabel("ano")
# plt.ylabel("população")
# plt.show()
