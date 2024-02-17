import os
import pickle
import shutil
import json

SOGLIA_SCORE = 0.42
# Ottieni il percorso assoluto della directory corrente
absPath = os.path.dirname(os.path.abspath(__file__))

# Definisci la directory dei match e ottieni tutti i file presenti
MATCHES_DIRECTORY = absPath + "/matches-hw3"
allMatches = os.listdir(MATCHES_DIRECTORY)

# Inizializza un dizionario per memorizzare i match con score superiore a 0.33
matches = dict()
for fileName in allMatches:
    filePath = MATCHES_DIRECTORY + "/" + fileName
    with open(filePath, 'rb') as pickleFile:
        m = pickle.load(pickleFile)
    # Filtra i match con score superiore a 0.33 e memorizzali nel dizionario 'matches'
    for key in m:
        score = m[key]
        if score > SOGLIA_SCORE:
            matches[key] = score

# Inizializza una lista per memorizzare i set di attributi mediati
sets = []
for key in matches:
    dataset0, dataset1 = key
    combined = set()
    combined.add(dataset0)
    combined.add(dataset1)
    # Unisci i set se uno degli attributi è già presente in un set
    for s in sets:
        if dataset0 in s or dataset1 in s:
            combined = combined.union(s)
            sets.remove(s)
    sets.append(combined)

# Crea una nuova directory per i match processati
PROCESSED_MATCHES_DIRECTORY = absPath + "/processed_matches"
if os.path.exists(PROCESSED_MATCHES_DIRECTORY):
    shutil.rmtree(PROCESSED_MATCHES_DIRECTORY)
os.mkdir(PROCESSED_MATCHES_DIRECTORY)

# Scrivi i set di attributi mediati nei file di output
for i, s in enumerate(sets):
    fileName = "matches" + str(i) + ".txt"
    filePath = PROCESSED_MATCHES_DIRECTORY + "/" + fileName
    with open(filePath, 'w') as f:
        for elem in s:
            f.write(str(elem) + '\n')

# Chiedi all'utente di assegnare un nome a ciascun set di attributi mediati
labelsMediatedSchema = []
for s in sets:
    print(s)
    print("Qual è il nome che desideri dare a questo insieme di attributi?")
    name = input()
    print()
    labelsMediatedSchema.append(name)

# Ottieni lo schema dei dati dai file JSON presenti nella directory
SOURCES_DIRECTORY = "/Users/fspezzano/vscode/id-hw6/hw3_integration/tabelle_parsate"
files = os.listdir(SOURCES_DIRECTORY)
schemas = []
for file in files:
    filePath = SOURCES_DIRECTORY + "/" + file
    with open(filePath, 'r') as jsonfile:
        data = json.load(jsonfile)[0]
    # Assegna etichette ai campi dello schema in base ai set di attributi mediati
    for key in data:
        label = None
        for i, s in enumerate(sets):
            for elem in s:
                dataset, column = elem
                if dataset != file:
                    continue
                if key != column:
                    continue
                label = labelsMediatedSchema[i]
                break
            if label:
                break
        if not label:
            print(f"{key} da {file} richiede un'etichetta, inserisci l'etichetta desiderata:")
            label = input()
        data[key] = label
    data["dataset"] = file
    schemas.append(data)

# Scrivi lo schema mediato in un file JSON
mediatedSchemaPath = absPath + "/json/mediated_schema-hw3.json"
if os.path.exists(mediatedSchemaPath):
    os.remove(mediatedSchemaPath)
with open(mediatedSchemaPath, "w") as json_file:
    json.dump(schemas, json_file, indent=4)