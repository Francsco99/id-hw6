import json
import os

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/final_table_lower.json'
OUTPUT_FOLDER = os.path.join(ABS_PATH, "json/country_blocks")

#Lettura file json
def readJsonFile(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data

#Salvataggio file json
def saveJsonFile(data, output_file):
    with open(output_file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)

# Assicurati che la cartella di output esista
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

#Cerca elemento nel dizionario
def searchCountryRighe(element, country, country_righe):
    if country in country_righe:
        country_righe[country].append(element)
    else:
        country_righe[country] = [element]

#Divide file di input in blocchi in base alla country
def countryBlocking(data):
    dizionario={}
    for element in data:
        country = element["country"]
        if not country:
            searchCountryRighe(element,"unknown",dizionario)
        else:
            searchCountryRighe(element,country,dizionario)
    return dizionario

#file di input
data = readJsonFile(INPUT_FOLDER)
#dizionario contenente country->elementi
dizionario = countryBlocking(data)

#salvataggio file con nome del paese
for paese in dizionario.keys():
    output_file_path = os.path.join(OUTPUT_FOLDER, f"{paese}.json")
    saveJsonFile(dizionario[paese], output_file_path)