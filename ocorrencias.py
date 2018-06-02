import MySQLdb
import datetime
import pandas as pd

from os import listdir, getcwd
from os.path import isfile, join


current_dir = getcwd()
src_dir = join(current_dir, 'src')
output_dir = join(current_dir, 'output')

conn = MySQLdb.connect(host = "0.tcp.ngrok.io",
                       port = 18848,
                       user = "root",
                       passwd = "senha",
                       db = "empregos")

cursor = conn.cursor()

only_files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]

queries = []

print('inico')
for file in only_files:
    df = pd.read_csv(join(src_dir, file), encoding='iso-8859-15', sep=';')

    print(file)
    for index, row in df.iterrows():
        sigla_estado = """ SELECT id FROM empregos.estado WHERE sigla LIKE '%s' """ % (row["Sigla UF"])
        cursor.execute(sigla_estado)
        selectCodigo = list(cursor.fetchall())
        estadoId = selectCodigo[0][0]



        regiao = """ SELECT id FROM empregos.regiao WHERE nome LIKE '%s'  """ % (row["Região"])
        cursor.execute(regiao)
        selectRegiao = list(cursor.fetchall())
        regiaoId = selectRegiao[0][0]

        data = row['Mês/Ano'].split('/')
        data = datetime.date(int(data[1]), int(data[0]), 1)

        t_crime = str(row["Tipo Crime"])
        crime = """ SELECT id FROM empregos.crime WHERE crime LIKE '%s' """ % (t_crime)
        cursor.execute(crime)
        selectCrime = list(cursor.fetchall())

        try:
            tipoCrime = selectCrime[0][0]
        except:
            print(crime, selectCrime)

        query_insert = """INSERT INTO empregos.ocorrencia (regiaoId, estadoId, codigoIbge, municipio, tipo_crime, quantidade, data) VALUES (%s, %s, %s, '%s', '%s', %s, '%s');\n""" % (regiaoId, estadoId, row["Código IBGE Município"], row["Município"], tipoCrime, row["PC-Qtde Ocorrências"], data)
        queries.append(query_insert)
        # cursor.execute(query_insert)
        # conn.commit()

conn.close()

print('escrevendo')
with open(join(output_dir, "script.sql"), mode='w') as file:
    file.writelines(queries)
print('finalizado')
