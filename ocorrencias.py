import threading
import MySQLdb
import pandas as pd

from datetime import datetime, date
from os import listdir, getcwd
from os.path import isfile, join

threads = []
Num_Of_threads = 5

current_dir = getcwd()
src_dir = join(current_dir, 'src')
output_dir = join(current_dir, 'output')

only_files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]


class Thread(threading.Thread):

    def __init__(self, conn, cur, file):
        threading.Thread.__init__(self)
        self.conn = conn
        self.cur = cur
        self.file = file
        self.queries = []

    def write_output_file(self):
        file_name = '{}.sql'.format(self.file.split('.')[0])
        with open(join(output_dir, file_name), mode='w') as file:
            file.writelines(self.queries)

    def run(self):
        print(self.file, datetime.now())

        df = pd.read_csv(join(src_dir, self.file), encoding='iso-8859-15', sep=';')

        for index, row in df.iterrows():
            sigla_estado = "SELECT id FROM empregos.estado WHERE sigla LIKE '{}'".format(row["Sigla UF"])
            self.cur.execute(sigla_estado)
            selectCodigo = self.cur.fetchone()
            estadoId = selectCodigo[0]

            regiao = """ SELECT id FROM empregos.regiao WHERE nome LIKE '%s'  """ % (row["Região"])
            self.cur.execute(regiao)
            selectRegiao = list(self.cur.fetchall())
            regiaoId = selectRegiao[0][0]

            data = row['Mês/Ano'].split('/')
            data = date(int(data[1]), int(data[0]), 1)

            t_crime = str(row["Tipo Crime"])
            crime = """ SELECT id FROM empregos.crime WHERE crime LIKE '%s' """ % (t_crime)
            self.cur.execute(crime)
            selectCrime = list(self.cur.fetchall())

            try:
                tipoCrime = selectCrime[0][0]
            except:
                print(crime, selectCrime)

            query_insert = """INSERT INTO empregos.ocorrencia (regiaoId, estadoId, codigoIbge, municipio, tipo_crime, quantidade, data) VALUES (%s, %s, %s, '%s', '%s', %s, '%s');\n""" % (
            regiaoId, estadoId, row["Código IBGE Município"], row["Município"], tipoCrime, row["PC-Qtde Ocorrências"], data)
            self.queries.append(query_insert)

            if len(self.queries) > 10:
                break

        print('escrevendo', datetime.now())
        self.write_output_file()
        print('finalizado', datetime.now())


for i in range(Num_Of_threads):
    conn = MySQLdb.connect(host="0.tcp.ngrok.io",
                           port=16788,
                           user="root",
                           passwd="senha",
                           db="empregos")
    cursor = conn.cursor()

    new_thread = Thread(conn, cursor, only_files[i])
    threads.append(new_thread)

for th in threads:
    th.start()

for th in threads:
    th.join()
