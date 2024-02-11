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
INPUT_FOLDER = os.path.join(ABS_PATH, "outp.json")
OUTPUT_FOLDER = os.path.join(ABS_PATH, "output") # Modificato per includere una sottocartella "output"

# Assicurati che la cartella di output esista
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Funzioni rimangono invariate

# Correzione nella funzione searchDateRighe per utilizzare match.group()
def searchDateRighe(element, year, date_righe):
    if year in date_righe:
        date_righe[year].append(element)
    else:
        date_righe[year] = [element]

# Aggiornamento della funzione dataBlocking per gestire correttamente match.group()
def dataBlocking(data, dizionario, lista):
    for element in data:
        anno_fondazione = str(element["found_year"])
        if (len(anno_fondazione) == 4) and (anno_fondazione[0] in ["1", "2"]):  # tipo 2005 o 1999
            searchDateRighe(element, anno_fondazione, dizionario)
        else:
            pattern = r'(?<!\d)\d{4}(?!\d)'
            match = re.search(pattern, anno_fondazione)
            if match:
                searchDateRighe(element, match.group(), dizionario)  # Uso match.group() per ottenere la stringa
            else:
                searchDateRighe(element, "unknown", dizionario)  # Uso "unknown" per anni non identificabili
                if not(element["found_year"]):
                    lista.append(element)

data = readJsonFile(INPUT_FOLDER)
date_righe = {}
problemi = []

dataBlocking(data, date_righe, problemi)
print(date_righe.keys())
# Salvataggio del file JSON
output_file_path = os.path.join(OUTPUT_FOLDER, "found_year_block.json")  # Definizione del percorso del file di output
saveJsonFile(date_righe, output_file_path)  # Salvataggio del file
