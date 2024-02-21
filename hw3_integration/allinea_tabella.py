import json

INPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/hw3_integration/json/final_table-hw3.json'
OUTPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/hw3_integration/json/final_table-hw3_alinged-last.json'
TABELLA_FINALE_PATH = '/Users/fspezzano/vscode/id-hw6/pairwise_matching/json/final_table_company_name.json'

def readJson(file_path):
    """Funzione per leggere un file JSON e restituire i dati."""
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def saveFile(tabella,out_path):
    with open(out_path, "w") as json_file:
        json.dump(tabella, json_file, indent=4)

tabella_finale = readJson(TABELLA_FINALE_PATH)

colonne_finali = []
for element in tabella_finale:
    for attributo in element:
        colonne_finali.append(attributo)
    break

tabella_hw3 = readJson(INPUT_FOLDER)
tabella_nuova=[]

for el in tabella_hw3:
    new_element = {}
    for attr in el:
        if attr in colonne_finali:
            new_element[attr] = el[attr]
    tabella_nuova.append(new_element)

last_tabella = []
for riga in tabella_nuova:
    new_element = {}
    # Ensure all keys from colonne_finali are in the new element
    for at in colonne_finali:
        # Check if the attribute is in the current row, else assign an empty string
        new_element[at] = riga.get(at, "")
    last_tabella.append(new_element)

lastlast = tabella_finale+last_tabella
saveFile(lastlast,OUTPUT_FOLDER)
    

