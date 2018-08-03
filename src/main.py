import glob
import os
from os.path import join
import pandas as pd

from src.data_sources.dataframes_crimes_desempregos import getDesligadosUF, getOcorrenciasByCrime, getPopulacao
from src.data_sources.dataframes_empregos import getDataFramesEmpregos
from src.data_sources.dataframes_ocorrencias import generateHeatMapBrazilOcorrencias, getDataframesOcorrenciasCrime, \
    getDataframesTotalOcorrencias
from src.data_sources.dataframes_população import getDataframePopState, getDataframeRegions
from src.utils.utils import ARQUIVOS_OCORRENCIAS, ANOS, CRIMES, CATEGORIAS_EMPREGOS, ESTADOS_SIGLAS, REGIOES
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


colorsIBGE = ['mediumblue', 'red', 'lime', 'purple', 'grey', 'black', 'darkolivegreen']
axIBGE = None

"""
Dataframes base
"""
# Dataframe de população
dfs_populacao = list(map(getDataframePopState, ANOS))
df_populacao = pd.concat(dfs_populacao)
## Dataframe população por região
lista_dfs_regioes_populacao = getDataframeRegions()


# Dataframe de empregos
dfs_empregos = getDataFramesEmpregos()

# Dataframe de ocorrências
dfs_ocorrencias = getDataframesTotalOcorrencias()
dfs_ocorrencias['ano_ocorrencia'] = dfs_ocorrencias.Mês_Ano.str[3:]


"""
Processamento de dados
"""


def createDataframePopulacaoRegiaoGenero(dataframe):
    df_columns_filtered = dataframe.iloc[3:, 11:16]
    region_name = dataframe.columns.values[0].split()[-1]

    # Dataframe população masculina
    df_total_men = df_columns_filtered.iloc[1]
    df_total_men_2010 = df_total_men.iloc[0]
    # Dataframe com a proporção masculina em relação a 2010
    df_proporcao_men = list(map(lambda x: ((x / df_total_men_2010) * 100) - 100, df_total_men))


    # Dataframe população feminina
    df_total_women = df_columns_filtered.iloc[24]
    df_total_women_2010 = df_total_women.iloc[0]
    # Dataframe com a proporção feminina em relação a 2010
    df_proporcao_women = list(map(lambda x: ((x / df_total_women_2010) * 100) - 100, df_total_women))

    p1 = plt.bar(ANOS, df_proporcao_men, 0.8, color='c')
    p2 = plt.bar(ANOS, df_proporcao_women, 0.8, bottom=df_proporcao_men, color='y')

    plt.xlabel("Ano")
    plt.ylabel("Taxa de variação de população em %")
    plt.legend((p1[0], p2[0]), ('Masculino', 'Feminino'))

    plt.plot()
    plt.savefig(f'graficos/populacao/genero/{region_name}.png')
    plt.gcf().clear()


"""
Plot
"""


def plotTaxaDesempregoFaixaEtaria(categorias):
    for categoria in categorias:
        dataframe = dfs_empregos[categoria]
        dataframe_groupby = dataframe.groupby('ano')['valor'].sum()
        dataframe_proporcao = list(map(lambda x: ((x / dataframe_groupby.iloc[0]) * 100) - 100, dataframe_groupby))
        plt.bar(ANOS, dataframe_proporcao, 0.8, color='b')
        plt.xlabel("Ano")
        plt.ylabel("Taxa de variação de desemprego em %")
        plt.plot()
        categoria_sem_barra = categoria.replace("/", "_")
        plt.savefig(f'graficos/desemprego/faixa_etaria/{categoria_sem_barra}.png')
        plt.gcf().clear()


def plotEmpregosOcorrencias(setor):
    global dfs_empregos

    df_emprego = [d[setor] for d in dfs_empregos if setor in d]
    df_join_empregos_ocorrencias = pd.merge(df_emprego[0],
                                            dfs_ocorrencias,
                                            on=['estado_ibge', 'ano'],
                                            how='inner')
    # df_join_empregos_ocorrencias = pd.merge(dfs_empregos[setor],
    #                                         dfs_ocorrencias,
    #                                         on=['estado_ibge', 'ano'],
    #                                         how='inner')

    df_groupby_empregos_ocorrencias = df_join_empregos_ocorrencias.groupby(
        ['UF', 'Tipo_Crime', df_join_empregos_ocorrencias['ano_ocorrencia'], 'populacao'])[
        'PC-Qtde_Ocorrências'].sum().reset_index(name='ocorrencias')

    df_merge = pd.merge(df_emprego[0],
                        df_populacao,
                        on=['estado_ibge', 'ano'])
    # df_merge = pd.merge(dfs_empregos[setor],
    #                     df_populacao,
    #                     on=['estado_ibge', 'ano'])

    df_groupby_empregos_ocorrencias['prop_ocorrencias'] = df_groupby_empregos_ocorrencias['ocorrencias'] / df_groupby_empregos_ocorrencias['populacao']

    df_merge['prop_desempregados'] = df_merge['valor'] / df_merge['populacao']

    setor_sem_barra = setor.replace("/", "_")
    # os.makedirs(f'graficos/{setor_sem_barra}')

    # TODO - Retirar os fors
    for key, value in ESTADOS_SIGLAS.items():
        for crime in CRIMES:
            handlesIBGE = []

            df1 = df_groupby_empregos_ocorrencias.loc[(df_groupby_empregos_ocorrencias.UF == value) &
                                                      (df_groupby_empregos_ocorrencias.Tipo_Crime == crime)]
            df2 = df_merge.loc[(df_merge.Sigla_UF == key)]

            x = df1['ano_ocorrencia']
            y = df1['prop_ocorrencias'] * 100
            y2 = df2['prop_desempregados'] * 100

            if len(x) != len(y2):
                print(f'Dados inconsistentes de {value} para o crime {crime}')
            else:
                plt.plot(x, y, color='mediumblue')
                plt.plot(x, y2, color='lime')

                patch1 = mpatches.Patch(color='mediumblue', label='Ocorrências')
                patch2 = mpatches.Patch(color='lime', label='Desempregados')

                handlesIBGE.append(patch1)
                handlesIBGE.append(patch2)

                plt.legend(title='Taxas', handles=handlesIBGE)

                plt.xlabel("Ano")
                plt.ylabel("Proporção relacionada ao total de habitantes em %")
                plt.savefig(f'graficos/{setor_sem_barra}/{value}_{crime}')
            plt.gcf().clear()


list(map(plotEmpregosOcorrencias, CATEGORIAS_EMPREGOS))

# mulheres = total é posicao 24, homens = total é posicao 1
# list(map(createDataframePopulacaoRegiao, lista_dfs_regioes_populacao))
# plotTaxaDesemprego(CATEGORIAS_EMPREGOS[2:9])
# list(map(generateHeatMapBrazilOcorrencias, ARQUIVOS_OCORRENCIAS))
# print(getDesligadosUF())
# print(getOcorrenciasByCrime())
# print(getPopulacao())

#d for d in exampleSet if d['type'] in keyValList