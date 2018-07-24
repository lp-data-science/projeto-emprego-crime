import pandas as pd
from src.data_sources.dataframes_empregos import getDataFramesEmpregos
from src.data_sources.dataframes_ocorrencias import generateHeatMapBrazilOcorrencias, getDataframesOcorrenciasCrime, \
    getDataframesTotalOcorrencias
from src.data_sources.dataframes_população import getDataframePopState, getDataframePopState2
from src.utils.utils import ARQUIVOS_OCORRENCIAS, ANOS, CRIMES, CATEGORIAS_EMPREGOS
import matplotlib.pyplot as plt




dfs_populacao = list(map(getDataframePopState2, ANOS))

df_pop = pd.concat(dfs_populacao)

df_empregos = getDataFramesEmpregos()
df_ocorrencias = getDataframesTotalOcorrencias()

df_ocorrencias['ano_ocorrencia'] = df_ocorrencias.Mês_Ano.str[3:]

df_ocorrencias_group = df_ocorrencias.groupby(['CD_GEOCUF', 'Tipo_Crime', 'ano_ocorrencia'])['PC-Qtde_Ocorrências'].sum()

df_join_empregos_ocorrencias = df_ocorrencias.join(df_empregos['Setor IBGE, Comércio - Admitidos/Desligados, Desligado']. set_index('estado_ibge'),
                                                   on='CD_GEOCUF')


df_groupby = df_join_empregos_ocorrencias.groupby(['UF', 'Tipo_Crime', df_join_empregos_ocorrencias['ano_ocorrencia'], 'populacao'])[
        'PC-Qtde_Ocorrências'].sum().reset_index(name='ocorrencias')


# df_groupby.rename(columns={'valor': 'desempregados'}, inplace=True)

df_groupby2 = df_join_empregos_ocorrencias.groupby(['UF', df_join_empregos_ocorrencias['ano_ocorrencia'], 'populacao'])[
        'valor'].sum().reset_index(name='desempregados')


df_empregos['Setor IBGE, Comércio - Admitidos/Desligados, Desligado'].rename(columns={'estado_ibge': 'CD_GEOCUF'}, inplace=True)
df_merge = pd.merge(df_empregos['Setor IBGE, Comércio - Admitidos/Desligados, Desligado'],
                    df_pop,
                    on=['CD_GEOCUF', 'ano'])

df_groupby2['prop_desempregados'] = df_groupby2['desempregados'] / df_groupby2['populacao']
df_groupby['prop_ocorrencias'] = df_groupby['ocorrencias'] / df_groupby['populacao']

# print(df_groupby2['desempregados'])
# print(df_groupby2.iloc[727])

df_merge['prop_desempregados'] = df_merge['valor'] / df_merge['populacao']


print(df_merge['prop_desempregados'])

df_uf = df_groupby.loc[(df_groupby.UF == 'Rio de Janeiro') & (df_groupby.Tipo_Crime == 'Estupro')]
df_uf2 = df_merge.loc[(df_merge.UF == 'RJ')]

x = df_uf['ano_ocorrencia']
y = df_uf['prop_ocorrencias']
print(len(x))
print(len(y))

y2 = df_uf2['prop_desempregados']
print(len(y2))
plt.plot(x, y)
plt.plot(x, y2)

plt.show()
