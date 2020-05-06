from os import listdir
import json

path = "/media/joaorura/7016D4F016D4B7F4/Workspace/Data/theTest"

json_file = {}

def listar_arquivos(caminho=None):
    lista_arqs = [arq for arq in listdir(caminho)]
    return lista_arqs

list_of_files = listar_arquivos(path)

with open('recommender_database.json', 'w') as file:
  vector = []
  for i in list_of_files:

    string = i.lower()
    string = string[:-7]
    with open (str(path) + '/' + str(i), 'r') as file_code:
      code = file_code.read()
      json_aux = {}
      json_aux["method_name"] = string
      json_aux["method_code"] = code
      vector.append(json_aux)  
  json.dump(vector, file, indent=4)

