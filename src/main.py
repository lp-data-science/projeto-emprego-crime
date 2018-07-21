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

df_ocorrencias['ano_ocorrencia'] = df_ocorrencias.Mês_Ano.str[3:]

df_ocorrencias_group = df_ocorrencias.groupby(['CD_GEOCUF', 'Tipo_Crime', 'ano_ocorrencia'])['PC-Qtde_Ocorrências'].sum()

df_join_empregos_ocorrencias = df_ocorrencias.join(df_empregos['Setor IBGE, Comércio - Admitidos/Desligados, Desligado'].set_index('estado_ibge'),
                                                   on='CD_GEOCUF')


df_groupby = df_join_empregos_ocorrencias.groupby(['UF', 'Tipo_Crime', 'ano_ocorrencia', 'valor', 'populacao'])[
        'PC-Qtde_Ocorrências'].sum().reset_index(name='ocorrencias')


df_groupby.rename(columns={'valor': 'desempregados'}, inplace=True)

df_groupby['prop_desempregados'] = df_groupby['desempregados'] / df_groupby['populacao']
df_groupby['prop_ocorrencias'] = df_groupby['ocorrencias'] / df_groupby['populacao']

# df_props = df_groupby.loc[:, ['prop_desempregados', 'prop_ocorrencias']]
#
# df_props = df_props.transpose()
#
# x, y = df_props.T

df_pe = df_groupby.loc[(df_groupby.UF == 'Pernambuco') & (df_groupby.Tipo_Crime == 'Estupro')]

# df_groupby_pe = df_pe.groupby(['ano'])['ocorrencias'].sum()


# for i in range(20):
#     print(df_pe.iloc[i])
#
# print(df_groupby_pe)

# print(df_groupby_pe.iloc[0])

par = list(zip(df_groupby['prop_ocorrencias'], df_groupby['prop_desempregados']))

print(len(par))
#
# plt.plot(par)

# fig,ax = plt.subplots()
#
# for name in CRIMES:
#     ax.plot(df_groupby[df_groupby.Tipo_Crime==name].ano,df_groupby[df_groupby.Tipo_Crime==name].prop_ocorrencias,label=name)
#
# ax.set_xlabel("ano")
# ax.set_ylabel("prop_ocorrencias")
# ax.legend(loc='best')

# plt.plot('desempregados', 'ocorrencias', data=df_groupby, marker='o')

plt.show()
