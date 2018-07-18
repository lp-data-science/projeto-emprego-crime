from pprint import pprint
from os import listdir, getcwd
from os.path import isfile, join
import requests
import json

contador = 0

current_dir = getcwd()
empregos_dir = join(current_dir, "dados_empregos")

def get_json_file_empregos(link):
    global contador
    headers = {'Accept': 'application/json'}
    response = requests.get(link, headers=headers)
    file_name = response.json()["nome"].replace("/", "_").replace(",", "_").replace(" ", "_") + ".json"
    contador += 1
    json_file = response.json()
    with open(join(empregos_dir, file_name), 'w') as f:

        f.write(str(json_file).replace("\'", "\"").replace("False", "0").replace("True", "1"))

#########################################################################################################
## Jsons da base de empregos ##
#########################################################################################################
for i in range(3,54):
    if i < 10:
        link = 'http://api.pgi.gov.br/api/1/serie/20970%s' % (i)
    else:
        link = 'http://api.pgi.gov.br/api/1/serie/2097%s' % (i)
    get_json_file_empregos(link)

#########################################################################################################
## Teste ##
#########################################################################################################
with open(join(empregos_dir, 'Número_de_Admitidos_Desligados_por_UF__Faixa_Etária_até_17_Anos_-_Admitidos_Desligados__Ad.json')) as of:
    data = json.load(of)
pprint(data)