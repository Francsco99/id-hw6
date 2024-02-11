import os
import json

# Ottieni il percorso assoluto della directory corrente
absPath = os.path.dirname(os.path.abspath(__file__))

# Carica il ground truth dai dati esterni
groundTruthPath = os.path.join(os.path.dirname(absPath), "/json/ground_truth.json")
with open(groundTruthPath, 'r') as jsonfile:
    groundTruth = json.load(jsonfile)

# Carica lo schema mediato dal file JSON
mediatedSchemaPath = os.path.join(absPath, "/json/mediated_schema.json")
with open(mediatedSchemaPath, 'r') as jsonfile:
    mediatedSchema = json.load(jsonfile)

# Conversione dello schema mediato in un dizionario con il nome del dataset come chiave
temp = {}
for schema in mediatedSchema:
    if "dataset" in schema:  # Controllo per evitare KeyError
        name = schema.pop("dataset")
        temp[name] = schema
mediatedSchema = temp

# Conversione del ground truth in un dizionario simile, utilizzando lo stesso formato
temp = {}
for schema in groundTruth:
    if "dataset" in schema:  # Controllo per evitare KeyError
        name = schema.pop("dataset")
        temp[name] = schema
groundTruth = temp

# Inizializzazione delle variabili per il conteggio delle discrepanze
wrongOnes = 0
totalAttributesChecked = 0

# Confronto degli attributi nei due schemi e conteggio delle discrepanze
for datasetName in mediatedSchema:
    schema = mediatedSchema[datasetName]
    for attribute in schema:
        totalAttributesChecked += 1
        # Controlla se l'attributo esiste nel ground truth e se i nomi degli attributi corrispondono
        if attribute not in groundTruth[datasetName] or schema[attribute] != groundTruth[datasetName][attribute]:
            wrongOnes += 1
            # Stampa le discrepanze trovate
            print("This one is different from ground truth:")
            print(f"Dataset name: {datasetName}")
            print(f"Attribute: {attribute}")
            print(f"Ground truth: {groundTruth[datasetName].get(attribute, 'N/A')}")
            print(f"Given name: {schema[attribute]}")
            print()

# Calcolo della precisione in base alle discrepanze trovate
precision = 1 - (wrongOnes / totalAttributesChecked) if totalAttributesChecked else 0

# Stampa delle statistiche
print("\nStatistics")
print(f"Number of wrong namings: {wrongOnes}")
print(f"Number of total attributes checked: {totalAttributesChecked}")
print(f"Precision: {precision}")