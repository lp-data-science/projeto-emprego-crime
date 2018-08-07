import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from src.data_sources.dataframes_empregos import getDataFramesEmpregos
from src.data_sources.dataframes_ocorrencias import getDataframesTotalOcorrencias, getDataframesOcorrenciasAno, ESTADOS_DIR
from src.data_sources.dataframes_população import getDataframePopState, getDataframeRegions
from src.utils.utils import ANOS, CRIMES, ESTADOS_SIGLAS


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

#Dataframe principal
df_result = pd.read_csv("data_sources/dados_crimes_desemprego/df_result.csv")


"""
Processamento de dados
"""


def calculateCorrelationCrimeDesempregoByState(UF):
    df = df_result.loc[df_result.Sigla_UF == UF]
    correlation = df["taxa_ocorrencia"].corr(df["taxa_desemprego"])
    print(f'{UF}: {correlation}')


"""
Plot
"""


def plotDataframePopulacaoRegiaoGenero(dataframe):
    """
    Função que plota gráficos de barra composta informando a variação da população, masculina e feminina, em relação
    a população mensurada em 2010
    :param dataframe: pandas.DataFrame
    """
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


def plotTaxaDesempregoFaixaEtaria(categoria):
    """
    Função que plota os gráficos de taxa de variação de desemprego em relação ao ano de 2010, por faixa etária
    :param categoria: String
    """
    dataframe = [d[categoria] for d in dfs_empregos if categoria in d] #TODO - FOR do list comprehension
    dataframe_groupby = dataframe[0].groupby('ano')['valor'].sum()
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

    df_emprego = [d[setor] for d in dfs_empregos if setor in d] #TODO - FOR do list comprehension
    df_join_empregos_ocorrencias = pd.merge(df_emprego[0],
                                            dfs_ocorrencias,
                                            on=['estado_ibge', 'ano'],
                                            how='inner')

    df_groupby_empregos_ocorrencias = df_join_empregos_ocorrencias.groupby(
        ['UF', 'Tipo_Crime', df_join_empregos_ocorrencias['ano_ocorrencia'], 'populacao'])[
        'PC-Qtde_Ocorrências'].sum().reset_index(name='ocorrencias')

    df_merge = pd.merge(df_emprego[0],
                        df_populacao,
                        on=['estado_ibge', 'ano'])

    df_groupby_empregos_ocorrencias['prop_ocorrencias'] = df_groupby_empregos_ocorrencias['ocorrencias'] / df_groupby_empregos_ocorrencias['populacao']

    df_merge['prop_desempregados'] = df_merge['valor'] / df_merge['populacao']

    setor_sem_barra = setor.replace("/", "_")
    os.makedirs(f'graficos/desemprego_ocorrencias/{setor_sem_barra}')

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
                plt.savefig(f'graficos/desemprego_ocorrencias/{setor_sem_barra}/{value}_{crime}')
            plt.gcf().clear()


def plotEstadoHeatMap(arquivo,df_groupby, crime):
    """
    Função que gera e salva os gráficos de mapas de calor em arquivo de imagem
    :param arquivo: String
    :param df_groupby: pandas.DataFrame
    :param crime: String
    :return: void
    """

    brazil_shape = gpd.read_file(ESTADOS_DIR)

    df_brazil_shape = pd.DataFrame(brazil_shape)
    df_brazil_shape["CD_GEOCUF"] = df_brazil_shape["CD_GEOCUF"].apply(int)
    df_brazil_shape.rename(columns={"CD_GEOCUF": "estado_ibge"}, inplace=True)

    df_join_groupby_shape = df_groupby.join(df_brazil_shape.set_index("estado_ibge"), on="estado_ibge_x")
    df_join_groupby_shape["proporcao"] = (df_join_groupby_shape.total / df_join_groupby_shape.populacao_x) * 100000

    geodf_join_groupby_shape = gpd.GeoDataFrame(df_join_groupby_shape[df_join_groupby_shape.Tipo_Crime == crime])
    geodf_join_groupby_shape.plot(column="proporcao", cmap="YlGnBu", legend=True)

    plt.title("Proporcao Crimes X Populacao")
    plt.savefig("graficos/graficos_ocorrencias/n_fig_{}_{}".format(crime, arquivo[-4:]))


def plotHeatMapBrazilOcorrencias(arquivo):
    """
    função que plota os gráficos dos crimes anualmente de forma proporcional
    :param arquivo: string
    :return: void
    """

    df_pop = getDataframePopState(arquivo[-4:])
    df_pop.rename(columns={'CD_GEOCUF': 'estado_ibge'})
    df_ocorrencia = getDataframesOcorrenciasAno(arquivo[-4:])
    df_ocorrencia_populacao = pd.merge(df_pop, df_ocorrencia, on="Sigla_UF", how="left", sort=False)
    df_groupby = df_ocorrencia_populacao.groupby(
        ['Tipo_Crime', 'Sigla_UF', 'estado_ibge_x', 'populacao_x'])[
        'PC-Qtde_Ocorrências'].sum().reset_index(name='total')

    list(map(lambda x: plotEstadoHeatMap(arquivo, df_groupby, x), CRIMES))


"""
Main
"""
##############
# Correlacao #
##############
# print(df_result.columns.values)
# df_result_corr = df_result.filter(["taxa_ocorrencia", "taxa_desemprego"], axis=1)
# l_corr = list(map(calculateCorrelationCrimeDesempregoByState, SIGLAS_UF))
#
# df_teste1 = df_result.filter(["Tipo_Crime", "ocorrencias", "Sigla_UF", "populacao", "taxa_ocorrencia", "taxa_desemprego"], axis=1)
#
#
# for UF in SIGLAS_UF:
#     for crime in CRIMES:
#         df = df_teste1.loc[(df_teste1.Sigla_UF == UF) & (df_teste1.Tipo_Crime == crime)]
#         correlation = df["taxa_ocorrencia"].corr(df["taxa_desemprego"])
#         df_teste1.loc[(df_teste1["Sigla_UF"] == UF) & (df_teste1.Tipo_Crime == crime), "corr"] = correlation
#
# corr = pd.DataFrame()
#
# for index, row in df_teste1.iterrows():
#     corr.loc[row["Sigla_UF"], row["Tipo_Crime"]] = row["corr"]
#
# print(corr)
#
# plt.pcolor(corr)
# plt.yticks(np.arange(0.5, len(corr.index), 1), corr.index)
# plt.xticks(np.arange(0.5, len(corr.columns), 1), corr.columns)
# plt.savefig("graficos/correlacao_por_crime_estado.png")
#
##############################################################


# list(map(plotTaxaDesempregoFaixaEtaria, getCategoriasFaixaEtaria()))

# list(map(plotHeatMapBrazilOcorrencias, ARQUIVOS_OCORRENCIAS))

# list(map(plotEmpregosOcorrencias, CATEGORIAS_EMPREGOS))

# mulheres = total é posicao 24, homens = total é posicao 1
# list(map(createDataframePopulacaoRegiao, lista_dfs_regioes_populacao))
# plotTaxaDesemprego(CATEGORIAS_EMPREGOS[2:9])
# list(map(generateHeatMapBrazilOcorrencias, ARQUIVOS_OCORRENCIAS))
# print(getDesligadosUF())
# print(getOcorrenciasByCrime())
# print(getPopulacao())



# df_ocorrencias = reduce(lambda df1,df2 : pd.concat([df1,df2], ignore_index=True, sort=True), dfs_ocorrencias)
# df_ocorrencias['ano'] = df_ocorrencias.Mes_Ano.str[3:]
# df_ocorrencias_group_by_estado = df_ocorrencias.groupby(["UF", df_ocorrencias['ano']])['PC-Qtde_Ocorrências'].sum().reset_index(name='ocorrencias')
# df_ocorrencias_group_by_crime = df_ocorrencias.groupby(["Tipo_Crime","UF"])['PC-Qtde_Ocorrências'].sum().reset_index(name='ocorrencias')
# df_ocorrencias_group_by_crime_ano = df_ocorrencias.groupby(["Tipo_Crime","UF","ano"])['PC-Qtde_Ocorrências'].sum().reset_index(name='ocorrencias')
#
# print(df_ocorrencias_group_by_crime_ano)