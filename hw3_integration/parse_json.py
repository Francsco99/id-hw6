import json
import os

INPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/hw3_integration/tabelle_hw3'
OUTPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/hw3_integration/tabelle_parsate'
def read_json_file(file_path):
    """Funzione per leggere un file JSON e restituire i dati."""
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def saveFile(tabella,out_path):
    with open(out_path, "w") as json_file:
        json.dump(tabella, json_file, indent=4)

def is_json_file(filename):
    _, file_extension = os.path.splitext(filename)
    return file_extension.lower() == '.json'   


#colonna1 : [valore1,valore1,...,valore1]
#colonna2: [valore2,valore2,...,valore2]
#colonna_n: [valore_n,...,valore_n]
#[{colonna1: valore1, colonna2: valore 2,...,colonna_n:valore n}]
def leggiTabella(data):
    colonne = data['columns']
    tabella=[]
    lunghezza = data['maxDimensions']['row']
    for i in range(lunghezza):
        temp={}
        j=0
        for colonna in colonne:
            if not colonna['columnName']:
                nome_colonna = f"colonna_{j}"
            nome_colonna=colonna["columnName"]
            temp[nome_colonna]=colonna["fields"][i]
        j+=1
        tabella.append(temp)
    return tabella

input_files = os.listdir(INPUT_FOLDER)

for file in input_files:
    #print("file corrente: ",file)
    input_path = os.path.join(INPUT_FOLDER, file)
    output_file = os.path.join(OUTPUT_FOLDER, file.replace('.json', '-proc.json'))
    if is_json_file(file):
        data = read_json_file(input_path)
        #tabella = leggiTabella(data)
        #saveFile(tabella,output_file)
        print(data['id'])