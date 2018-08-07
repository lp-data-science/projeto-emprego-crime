"""
FUNÇÕES AUXILIARES
"""
def getUFSigla(tuple_uf_state):
    return tuple_uf_state[0]


def getCategoriasFaixaEtaria():
    return list(filter(lambda x: x.split()[0] == "Faixa", CATEGORIAS_EMPREGOS))

"""
ENUMS
"""

CRIMES = [
    'Roubo seguido de morte (latrocínio)',
    'Roubo de veículo',
    'Lesão corporal seguida de morte',
    'Homicídio doloso',
    'Furto de veículo',
    'Estupro'
]

ANOS = [
    '2010',
    '2011',
    '2012',
    '2013',
    '2014'
]

ARQUIVOS_OCORRENCIAS = [
    'ocorrenciasmun-brasil2010',
    'ocorrenciasmun-brasil2011',
    'ocorrenciasmun-brasil2012',
    'ocorrenciasmun-brasil2013',
    'ocorrenciasmun-brasil2014'
]

CATEGORIAS_EMPREGOS = [
    'Faixa Etária Sem Classificação - Admitidos/Desligados, Desligado',
    'Faixa Etária até 17 Anos - Admitidos/Desligados, Admitido',
    'Faixa Etária até 17 Anos - Admitidos/Desligados, Desligado',
    'Faixa Etária com 65 Anos ou Mais - Admitidos/Desligados, Desligado',
    'Faixa Etária de 18 a 24 Anos - Admitidos/Desligados, Desligado',
    'Faixa Etária de 25 a 29 Anos - Admitidos/Desligados, Desligado',
    'Faixa Etária de 30 a 39 Anos - Admitidos/Desligados, Desligado',
    'Faixa Etária de 40 a 49 Anos - Admitidos/Desligados, Desligado',
    'Faixa Etária de 50 a 64 Anos - Admitidos/Desligados, Desligado',
    'Grau Instrução, 5ª Completo Fundamental - Admitidos/Desligados, Desligado',
    'Grau Instrução, 6ª a 9ª Fundamental - Admitidos/Desligados, Desligado',
    'Grau Instrução, Analfabeto - Admitidos/Desligados, Desligado',
    'Grau Instrução, Até 5ª Incompleto - Admitidos/Desligados, Desligado',
    'Grau Instrução, Fundamental Completo - Admitidos/Desligados, Desligado',
    'Grau Instrução, Médio Completo - Admitidos/Desligados, Desligado',
    'Grau Instrução, Médio Incompleto - Admitidos/Desligados, Desligado',
    'Grau Instrução, Superior Completo - Admitidos/Desligados, Desligado',
    'Grau Instrução, Superior Incompleto - Admitidos/Desligados, Desligado',
    'Setor IBGE, Administração Pública - Admitidos/Desligados, Desligado',
    'Setor IBGE, Agropecuária - Admitidos/Desligados, Admitido',
    'Setor IBGE, Agropecuária - Admitidos/Desligados, Desligado',
    'Setor IBGE, Comércio - Admitidos/Desligados, Admitido',
    'Setor IBGE, Comércio - Admitidos/Desligados, Desligado',
    'Setor IBGE, Construção Civil - Admitidos/Desligados, Desligado',
    'Setor IBGE, Extração Mineral - Admitidos/Desligados, Desligado',
    'Setor IBGE, Indústria de Transformação - Admitidos/Desligados, Desligado',
    'Setor IBGE, SERV IND UP - Admitidos/Desligados, Admitido',
    'Setor IBGE, SERV IND UP - Admitidos/Desligados, Desligado',
    'Sexo, Feminino - Admitidos/Desligados, Admitido',
    'Sexo, Feminino - Admitidos/Desligados, Desligado',
    'Sexo, Masculino - Admitidos/Desligados, Admitido',
    'Sexo, Masculino - Admitidos/Desligados, Desligado'
]

REGIOES = [
    "Norte",
    "Nordeste",
    "Centro-Oeste",
    "Sudeste",
    "Sul"
]



ESTADOS_SIGLAS = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AM': 'Amazonas',
    'AP': 'Amapá',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'PR': 'Paraná',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'RS': 'Rio Grande do Sul',
    'SC': 'Santa Catarina',
    'SE': 'Sergipe',
    'SP': 'São Paulo',
    'TO': 'Tocantins'
}

SIGLAS_UF = list(map(getUFSigla, ESTADOS_SIGLAS.items()))