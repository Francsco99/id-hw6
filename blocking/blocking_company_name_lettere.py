import json
import os
import re
import unicodedata as uc

# ABS_PATH e INPUT_FOLDER definiti 
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/pairwise_matching/annotation/file_ridotti/table_5-ridotta_1.json'
OUTPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/blocking/json/ridotto_name_blocks/file_1'

def readJsonFile(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data

def saveJsonFile(data, output_file):
    with open(output_file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)

def normalize_text(stringa):
    #pulisci = uc.normalize('NFKD', stringa).encode('ascii', 'ignore').decode('utf-8')
    name_pulito = re.sub(r'[^a-zA-Z0-9]', '', stringa)
    return name_pulito

def searchCompanyName(element, initial, company_names):
    if initial in company_names:
        company_names[initial].append(element)
    else:
        company_names[initial] = [element]

def organizeByCompanyNameQgram(data):
    dizionario={}
    for element in data:
        name = element['company_name']
        if not name:
            # Gestione dei casi in cui il nome dell'azienda non è disponibile
            searchCompanyName(element, "unknown", dizionario)  # Se il nome *prime due lettere* dell'azienda è presente
        else:
            norm_text = normalize_text(name)
            qgram = norm_text[:2]
            searchCompanyName(element, qgram, dizionario)
    return dizionario

data = readJsonFile(INPUT_FOLDER)
dizionario= organizeByCompanyNameQgram(data)


for qgram in dizionario.keys():
    output_file_path = os.path.join(OUTPUT_FOLDER, f"{qgram}.json")  # Definizione del percorso del file di output
    saveJsonFile(dizionario[qgram], output_file_path)  # Salvataggio del file

print("Elementi nel dizionario: ", len(dizionario))