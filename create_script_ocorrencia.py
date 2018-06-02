import unidecode
import pandas as pd

from multiprocessing import Process
from datetime import datetime, date
from os import listdir, getcwd
from os.path import isfile, join

process = []
num_of_process = 5

current_dir = getcwd()
src_dir = join(current_dir, 'src')
output_dir = join(current_dir, 'output')

csv_files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]


# TODO: Melhorar a representacao de crimes no banco e no codigo
crime = {
    'ROUBODEVEICULO': 5,
    'LESAOCORPORALSEGUIDADEMORTE': 4,
    'FURTODEVEICULO': 2,
    'ROUBOSEGUIDODEMORTE(LATROCINIO)': 6,
    'HOMICIDIODOLOSO': 3,
    'ESTUPRO': 1
}

estado = {
    'MG': 17, 'RN': 11, 'RR': 4, 'SP': 20,
    'PI': 9, 'RS': 23, 'SE': 15, 'SC': 22,
    'DF': 27, 'GO': 26, 'MT': 25, 'BA': 16,
    'PA': 5, 'AP': 6, 'PR': 21, 'RO': 1,
    'ES': 18, 'RJ': 19, 'AM': 3, 'TO': 7,
    'CE': 10, 'AC': 2, 'MA': 8, 'PB': 12,
    'PE': 13, 'MS': 24, 'AL': 14
}

regiao = {
    'NORTE': 1,
    'SUDESTE': 3,
    'SUL': 4,
    'CENTRO-OESTE': 5,
    'NORDESTE': 2
}


def run(csv):
    queries = []
    file_name = '{}.sql'.format(csv.split('.')[0])

    df = pd.read_csv(join(src_dir, csv), encoding='utf-8', sep=';')

    print(csv, datetime.now())
    for index, row in df.iterrows():
        estado_id = estado[row['Sigla UF']]
        regiao_id = regiao[row['Região']]

        data = row['Mês/Ano'].split('/')
        data = date(int(data[1]), int(data[0]), 1)

        tipo_crime = normalize_string(row["Tipo Crime"])
        crime_id = crime[tipo_crime]

        query_insert = 'INSERT INTO empregos.ocorrencia\
                       (regiaoId, estadoId, codigoIbge, municipio, tipo_crime, quantidade, data)\
                        VALUES (%s, %s, %s, "%s", "%s", %s, "%s");\n'\
                       % (regiao_id, estado_id, row["Código IBGE Município"], row["Município"], crime_id, row["PC-Qtde Ocorrências"], data)
        queries.append(query_insert)

    print('escrevendo', datetime.now())
    with open(join(output_dir, file_name), mode='w') as script:
        script.writelines(queries)
    print('finalizado', datetime.now())


def normalize_string(raw_str):
    data = unidecode.unidecode(raw_str)
    data = data.split()
    return ''.join(data).upper()


def multiprocess():
    processes = []

    for i in range(num_of_process):
        p = Process(target=run, args=(csv_files[i],))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()


if __name__ == "__main__":
    multiprocess()
