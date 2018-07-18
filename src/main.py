from src.data_sources.dataframes_ocorrencias import generateHeatMapBrazilOcorrencias
from src.utils.utils import ARQUIVOS_OCORRENCIAS, ANOS, CRIMES


x = list(map(generateHeatMapBrazilOcorrencias, ARQUIVOS_OCORRENCIAS))