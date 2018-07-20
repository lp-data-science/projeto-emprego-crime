import pandas as pd
from src.data_sources.dataframes_empregos import getDataFramesEmpregos
from src.data_sources.dataframes_ocorrencias import generateHeatMapBrazilOcorrencias, getDataframesOcorrenciasCrime, \
    getDataframesTotalOcorrencias
from src.utils.utils import ARQUIVOS_OCORRENCIAS, ANOS, CRIMES, CATEGORIAS_EMPREGOS
import matplotlib.pyplot as plt



# df_join = df_estupro_2010.join(data_frames['Faixa Etária de 18 a 24 Anos - Admitidos/Desligados, Desligado'].set_index('estado_ibge'),
#                                on='CD_GEOCUF').dropna()
# print(data_frames['Faixa Etária Sem Classificação - Admitidos/Desligados, Desligado'].columns.values)
# ax = data_frames['Faixa Etária Sem Classificação - Admitidos/Desligados, Desligado'].plot(x='ano', y='valor')
# print(data_frames['Faixa Etária de 18 a 24 Anos - Admitidos/Desligados, Desligado'])
# plt.plot('Sigla_UF', 'PC-Qtde_Ocorrências', data=df_estupro_2010, marker='o')
# df_estupro_2010.plot(x='Sigla_UF', y='PC-Qtde_Ocorrências')

df_empregos = getDataFramesEmpregos()
df_ocorrencias = getDataframesTotalOcorrencias()

df_join_empregos_ocorrencias = df_ocorrencias.join(df_empregos['Setor IBGE, Comércio - Admitidos/Desligados, Desligado'].set_index('estado_ibge'),
                                                   on='CD_GEOCUF')

df_groupby = df_join_empregos_ocorrencias.groupby(['Tipo_Crime', 'ano', 'UF', 'valor'])[
        'PC-Qtde_Ocorrências'].sum().reset_index(name='ocorrencias')

df_groupby.rename(columns={'valor': 'desempregados'}, inplace=True)

print(df_groupby.iloc[286])

# plt.show()
