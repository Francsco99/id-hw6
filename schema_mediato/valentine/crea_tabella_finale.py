import os
import json

# Ottieni il percorso assoluto della directory corrente
absPath = os.path.dirname(os.path.abspath(__file__))

# Percorso del file JSON contenente lo schema mediato
mediatedSchemaPath = "/Users/fspezzano/vscode/id-hw6/schema_mediato/valentine/json/mediated_schema-hw3.json"

# Carica lo schema mediato dal file JSON
with open(mediatedSchemaPath, 'r') as jsonfile:
    mediatedSchema = json.load(jsonfile)

# Rimuovi il campo "dataset" da ciascuno schema e memorizza lo schema mediato in un nuovo dizionario
temp = dict()
for schema in mediatedSchema:
    name = schema.pop("dataset")
    temp[name] = schema
mediatedSchema = temp

# Directory contenente i file JSON delle fonti
dataSource = "/Users/fspezzano/vscode/id-hw6/hw3_integration/tabelle_parsate"
files = os.listdir(dataSource)

# Estrai tutti gli attributi finali dall'insieme di schemi mediati
finalAttr = []
for schema in mediatedSchema.values():
    for value in schema.values():
        if value not in finalAttr:
            finalAttr.append(value)

# Costruisci la tabella finale combinando le voci dai file JSON delle fonti utilizzando lo schema mediato
finalTable = []
for file in files:
    filePath = dataSource + "/" + file
    with open(filePath, 'r') as jsonfile:
        entries = json.load(jsonfile)
    for entry in entries:
        temp = dict()
        # Mappa gli attributi dell'entry allo schema mediato
        for attr in mediatedSchema[file]:
            temp[mediatedSchema[file][attr]] = entry[attr]
        # Aggiungi gli attributi finali mancanti con valore vuoto
        for attr in finalAttr:
            if attr not in temp:
                temp[attr] = ""
        finalTable.append(temp)

# Percorso del file JSON finale
finalTablePath = absPath + "/json/final_table-hw3.json"

# Se esiste già un file finale, rimuovilo
if os.path.exists(finalTablePath):
    os.remove(finalTablePath)

# Salva la tabella finale in un nuovo file JSON
with open(finalTablePath, "w") as json_file:
    json.dump(finalTable, json_file, indent=4)