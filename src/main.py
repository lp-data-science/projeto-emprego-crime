from src.data_sources.dataframes_empregos import getDataFramesEmpregos
from src.data_sources.dataframes_ocorrencias import generateHeatMapBrazilOcorrencias, getDataframesOcorrenciasCrime
from src.utils.utils import ARQUIVOS_OCORRENCIAS, ANOS, CRIMES
import matplotlib.pyplot as plt


df_estupro_2010 = getDataframesOcorrenciasCrime("Estupro", 2010)
# data_frames = getDataFramesEmpregos()
# print(data_frames['Faixa Etária Sem Classificação - Admitidos/Desligados, Desligado'].columns.values)
# ax = data_frames['Faixa Etária Sem Classificação - Admitidos/Desligados, Desligado'].plot(x='ano', y='valor')

plt.plot('Sigla_UF', 'PC-Qtde_Ocorrências', data=df_estupro_2010, marker='o')
# df_estupro_2010.plot(x='Sigla_UF', y='PC-Qtde_Ocorrências')

plt.show()
