import pandas as pd
from src.data_sources.dataframes_empregos import getDataFramesEmpregos
from src.data_sources.dataframes_ocorrencias import generateHeatMapBrazilOcorrencias, getDataframesOcorrenciasCrime, \
    getDataframesTotalOcorrencias
from src.data_sources.dataframes_população import getDataframePopState
from src.utils.utils import ARQUIVOS_OCORRENCIAS, ANOS, CRIMES, CATEGORIAS_EMPREGOS, ESTADOS_SIGLAS
import matplotlib.pyplot as plt


"""
Dataframes base
"""
# Dataframe de população
dfs_populacao = list(map(getDataframePopState, ANOS))
df_populacao = pd.concat(dfs_populacao)

# Dataframe de empregos
dfs_empregos = getDataFramesEmpregos()

# Dataframe de ocorrências
dfs_ocorrencias = getDataframesTotalOcorrencias()
dfs_ocorrencias['ano_ocorrencia'] = dfs_ocorrencias.Mês_Ano.str[3:]

def teste(setor):
    # global df_populacao
    # global dfs_empregos
    # global dfs_ocorrencias

    df_join_empregos_ocorrencias = pd.merge(dfs_empregos[setor],
                                            dfs_ocorrencias,
                                            on=['estado_ibge', 'ano'],
                                            how='inner')

    df_groupby_empregos_ocorrencias = df_join_empregos_ocorrencias.groupby(
        ['UF', 'Tipo_Crime', df_join_empregos_ocorrencias['ano_ocorrencia'], 'populacao'])[
        'PC-Qtde_Ocorrências'].sum().reset_index(name='ocorrencias')

    df_merge = pd.merge(dfs_empregos[setor],
                        df_populacao,
                        on=['estado_ibge', 'ano'])

    df_groupby_empregos_ocorrencias['prop_ocorrencias'] = df_groupby_empregos_ocorrencias['ocorrencias'] / df_groupby_empregos_ocorrencias['populacao']

    df_merge['prop_desempregados'] = df_merge['valor'] / df_merge['populacao']

    for key, value in ESTADOS_SIGLAS.items():
        for crime in CRIMES:
            df1 = df_groupby_empregos_ocorrencias.loc[(df_groupby_empregos_ocorrencias.UF == value) &
                                                      (df_groupby_empregos_ocorrencias.Tipo_Crime == crime)]
            df2 = df_merge.loc[(df_merge.UF == key)]

            x = df1['ano_ocorrencia']
            y = df1['prop_ocorrencias']
            y2 = df2['prop_desempregados']

            if len(x) != len(y2):
                print("erro")
            else:
                plt.plot(x, y)
                plt.plot(x, y2)
                plt.savefig(f'graficos/{value}_{crime}')
            plt.gcf().clear()

teste('Setor IBGE, Administração Pública - Admitidos/Desligados, Desligado')