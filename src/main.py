import os
from functools import reduce

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from src.data_sources.dataframes_empregos import getDataFramesEmpregos, getDataFrameEmpregosFromJson
from src.data_sources.dataframes_ocorrencias import getDataframesTotalOcorrencias, getDataframesOcorrenciasAno, \
    ESTADOS_DIR, getDataFrameOcorrenciasFromCsv
from src.data_sources.dataframes_população import getDataframePopState, getDataframeRegions, \
    getDataFramePopulacaoFromCsv
from src.utils.utils import ANOS, CRIMES, ESTADOS_SIGLAS, SIGLAS_UF, ARQUIVOS_OCORRENCIAS, CATEGORIAS_EMPREGOS, \
    getCategoriasFaixaEtaria

colorsIBGE = ['mediumblue', 'red', 'lime', 'purple', 'grey', 'black', 'darkolivegreen']
axIBGE = None

"""
Funções auxiliares
"""


def creatListUfOcorrencias(uf):
    lista = list(map(lambda a: [uf, a], CRIMES))
    return lista


def creatListUfOcorrenciasAno(row):
    new_row = row
    lista = list(map(lambda ano: np.append(new_row, [ano]), ANOS))
    df_temp = pd.DataFrame(lista, columns=["Tipo_Crime", "UF", "ano"])
    return df_temp


def createRowUfOcorrenciasSemAno(row):
    new_row = pd.DataFrame({"UF": [row[0]], "Tipo_Crime": [row[1]]})
    return new_row


def getDataframePrincipal():
    df_populacao_principal = getDataFramePopulacaoFromCsv()
    df_desemprego_group_by_desligados_uf = getDataFrameEmpregosFromJson()
    df_ocorrencias_group_by_crime_ano = getDataFrameOcorrenciasFromCsv()

    list_temp = list(map(creatListUfOcorrencias, ESTADOS_SIGLAS.values()))
    list_row = reduce(lambda a, b: a + b, list_temp)
    list_df_temp = list(map(createRowUfOcorrenciasSemAno, list_row))

    df_base_uf_ocorrencia = reduce(lambda df1, df2: pd.concat([df1, df2], ignore_index=True, sort=True),
                                   list_df_temp)

    lista_dfs_com_ano = list(map(creatListUfOcorrenciasAno, df_base_uf_ocorrencia.values))

    df_base_uf_ocorrencia_ano = reduce(lambda df1, df2: pd.concat([df1, df2], ignore_index=True, sort=True),
                                       lista_dfs_com_ano)

    df_estado_ocorrencia_ano = pd.merge(df_base_uf_ocorrencia_ano, df_ocorrencias_group_by_crime_ano,
                                        on=["UF", "Tipo_Crime", "ano"], how='left')

    df_estado_ocorrencia_ano_populacao = pd.merge(df_estado_ocorrencia_ano, df_populacao_principal, on=["UF", 'ano'],
                                                  how='left')

    df_estado_ocorrencia_ano_populacao.rename(columns={'CD_GEOCUF': 'estado_ibge'}, inplace=True)

    ano_to_int = pd.to_numeric(df_estado_ocorrencia_ano_populacao.ano, errors='coerce')

    df_estado_ocorrencia_ano_populacao['ano'] = ano_to_int

    df_resultante = pd.merge(df_estado_ocorrencia_ano_populacao, df_desemprego_group_by_desligados_uf,
                         on=["estado_ibge", 'ano'], how='left')

    df_resultante['taxa_ocorrencia'] = df_resultante['ocorrencias'] / df_resultante['populacao'] * 100000
    df_resultante['taxa_desemprego'] = df_resultante['total_desempregados'] / df_resultante['populacao'] * 100000

    df_resultante.to_csv("df_result.csv")

    return df_resultante


def formatDataframeToPlotCorrelation(empty_df, tuple_df):
    empty_df.loc[tuple_df[1]["Sigla_UF"], tuple_df[1]["Tipo_Crime"]] = tuple_df[1]["corr"]


def getCorrelationDataframe(df_filtered, UF):
    dataframe_estado = df_filtered.loc[df_filtered.Sigla_UF == UF]
    list(map(lambda x: calculateCorrelationCrimeDesempregoPorEstado(df_filtered, dataframe_estado, UF, x), CRIMES))


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

# Dataframe principal
df_result = getDataframePrincipal()

"""
Processamento de dados
"""


def calculateCorrelationCrimeDesempregoPorEstado(main_dataframe, dataframe, UF, crime):
    dataframe_estado_crime = dataframe.loc[dataframe.Tipo_Crime == crime]
    correlation = dataframe_estado_crime["taxa_ocorrencia"].corr(dataframe_estado_crime["taxa_desemprego"])
    main_dataframe.loc[(main_dataframe["Sigla_UF"] == UF) & (main_dataframe.Tipo_Crime == crime), "corr"] = correlation


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
    dataframe = [d[categoria] for d in dfs_empregos if categoria in d]  # TODO - FOR do list comprehension
    dataframe_groupby = dataframe[0].groupby('ano')['valor'].sum()
    dataframe_proporcao = list(map(lambda x: ((x / dataframe_groupby.iloc[0]) * 100) - 100, dataframe_groupby))
    plt.bar(ANOS, dataframe_proporcao, 0.8, color='b')
    plt.title(categoria.split('-')[0])
    plt.xlabel("Ano")
    plt.ylabel("Taxa de variação de desemprego em %")
    plt.plot()
    categoria_sem_barra = categoria.replace("/", "_")
    plt.savefig(f'graficos/desemprego/faixa_etaria/{categoria_sem_barra}.png')
    plt.gcf().clear()


def get_all_chart_data(dfx, dfy, crime, setor_sem_barra):
    key, value = ESTADOS_SIGLAS.keys(), ESTADOS_SIGLAS.values()
    x = lambda value: dfx.loc[(dfx.UF == value) & (dfx.Tipo_Crime == crime)]
    y = lambda key: dfy.loc[(dfy.Sigla_UF == key)]
    df1 = list(map(x, value))
    df2 = list(map(y, key))

    list(map(plot_chart, df1, df2, value, [crime] * 27, [setor_sem_barra] * 27))


def plot_chart(df1, df2, value, crime, setor_sem_barra):
    handlesIBGE = []
    x = df1['ano_ocorrencia']
    y = df1['prop_ocorrencias'] * 100000
    y2 = df2['prop_desempregados'] * 100000

    if len(x) != len(y2):
        print(f'Dados inconsistentes de {value} para o crime {crime}')
    else:
        plt.title("Estado: {0}\nCrime: {1}".format(value, crime))
        plt.plot(x, y, color='mediumblue')
        plt.plot(x, y2, color='lime')

        patch1 = mpatches.Patch(color='mediumblue', label='Ocorrências')
        patch2 = mpatches.Patch(color='lime', label='Desempregados')

        handlesIBGE.append(patch1)
        handlesIBGE.append(patch2)

        plt.legend(title='Taxas', handles=handlesIBGE)

        plt.xlabel("Ano")
        plt.ylabel("Proporção (por 100.000 habitantes)")
        plt.savefig(f'graficos/desemprego_ocorrencias/{setor_sem_barra}/{value}_{crime}', dpi=300)
    plt.gcf().clear()


def plotEmpregosOcorrencias(setor):
    global dfs_empregos

    df_emprego = [d[setor] for d in dfs_empregos if setor in d]  # TODO - FOR do list comprehension
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

    df_groupby_empregos_ocorrencias['prop_ocorrencias'] = df_groupby_empregos_ocorrencias['ocorrencias'] / \
                                                          df_groupby_empregos_ocorrencias['populacao']

    df_merge['prop_desempregados'] = df_merge['valor'] / df_merge['populacao']

    setor_sem_barra = setor.replace("/", "_")

    try:
        os.makedirs(f'graficos/desemprego_ocorrencias/{setor_sem_barra}')
    except:
        print("Diretório já existe.")

    list(map(lambda x: get_all_chart_data(df_groupby_empregos_ocorrencias, df_merge, x, setor_sem_barra), CRIMES))


def plotEstadoHeatMap(arquivo, df_groupby, crime):
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

    df_join_groupby_shape = df_groupby.join(df_brazil_shape.set_index("estado_ibge"), on="estado_ibge")

    geodf_join_groupby_shape = gpd.GeoDataFrame(df_join_groupby_shape[df_join_groupby_shape.Tipo_Crime == crime])
    geodf_join_groupby_shape.plot(column="taxa_ocorrencia", cmap="YlGnBu", legend=True, vmin=0, vmax=160)

    plt.title(f'Proporção Crimes X População ({arquivo[-4:]})\n(a cada 100.000 habitantes)')
    plt.savefig(f'graficos/ocorrencias/fig_{crime}_{arquivo[-4:]}')
    plt.gcf().clear()

def plotHeatMapBrazilOcorrencias(arquivo):
    """
    função que plota os gráficos dos crimes anualmente de forma proporcional
    :param arquivo: string
    :return: void
    """
    global df_result

    df_result2 = df_result.loc[df_result.ano == int(arquivo[-4:])]
    list(map(lambda x: plotEstadoHeatMap(arquivo, df_result2, x), CRIMES))


def plotCorrelationMatrixHeatmap():
    """
    Função para plotar o heatmap da matriz de correlação entre taxa de desempregados e taxa de ocorrências, por estado
    :return: void
    """
    df_filtered = df_result.filter(
        ["Tipo_Crime", "ocorrencias", "Sigla_UF", "populacao", "taxa_ocorrencia", "taxa_desemprego"], axis=1)

    list(map(lambda x: getCorrelationDataframe(df_filtered, x), ESTADOS_SIGLAS))
    corr = pd.DataFrame()
    list(map(lambda x: formatDataframeToPlotCorrelation(corr, x), df_filtered.iterrows()))
    plt.title("Correlação de Taxa de ocorrências \ncom Taxa de desemprego")
    plt.pcolor(corr)
    plt.yticks(np.arange(0.5, len(corr.index), 1), corr.index, fontsize=7)
    plt.xticks(np.arange(0.5, len(corr.columns), 1), corr.columns, rotation=45, ha='right', fontsize=8)
    plt.tight_layout()
    plt.colorbar()
    plt.savefig("graficos/correlacao_por_crime_estado.png", dpi=300)
    plt.gcf().clear()


"""
Main
"""

# list(map(plotTaxaDesempregoFaixaEtaria, getCategoriasFaixaEtaria()))

# list(map(plotHeatMapBrazilOcorrencias, ARQUIVOS_OCORRENCIAS))

list(map(plotEmpregosOcorrencias, CATEGORIAS_EMPREGOS))

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
