import json
import os
import re

def readJsonFile(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data

def saveJsonFile(data, output_file):
    with open(output_file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)


# Supponendo che ABS_PATH e INPUT_FOLDER siano definiti come nel tuo script
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(ABS_PATH, "fixed_total.json")
OUTPUT_FOLDER = os.path.join(ABS_PATH, "output/block-paesi") # Modificato per includere una sottocartella "output"

# Assicurati che la cartella di output esista
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Funzioni rimangono invariate

# Correzione nella funzione searchDateRighe per utilizzare match.group()
def searchDateRighe(element, country, country_righe):
    if country in country_righe:
        country_righe[country].append(element)
    else:
        country_righe[country] = [element]


def countryBlocking(data,dizionario):
    for element in data:
        country = element["country"]
        if not country:
            searchDateRighe(element,"unknown",dizionario)
        else:
            searchDateRighe(element,country,dizionario)
        #if country == "['Cayman Islands', 'Hong Kong']":
            #print(element["company_name"])

data = readJsonFile(INPUT_FOLDER)
dizionario={}
countryBlocking(data,dizionario)

for paese in dizionario.keys():
    output_file_path = os.path.join(OUTPUT_FOLDER, f"{paese}.json")  # Definizione del percorso del file di output
    saveJsonFile(dizionario[paese], output_file_path)  # Salvataggio del file