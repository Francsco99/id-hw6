import json
import os
import pandas as pd
from valentine import valentine_match
from valentine.algorithms import Coma
import pickle
import re
import shutil

def read_json_file(file_path):
    """Funzione per leggere un file JSON e restituire i dati."""
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

# Percorso assoluto del file in esecuzione
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
# Percorso della directory dei file JSON delle tabelle
TABLES_PATH = os.path.join(ABS_PATH, "tables")
# Lista dei nomi dei file nella directory delle tabelle
file_names = os.listdir(TABLES_PATH)
# Dizionario per memorizzare i DataFrame delle tabelle
tables = {}

# Lettura dei file JSON delle tabelle e creazione dei DataFrame di Pandas
for file_name in file_names:
    file_path = os.path.join(TABLES_PATH, file_name)
    json_dict = read_json_file(file_path)
    table_name = json_dict["id"]
    cells = json_dict["cells"]
    rows = json_dict["maxDimensions"]["row"]
    columns = json_dict["maxDimensions"]["column"] + 1
    headers = ["" for _ in range(columns)]
    table_data = [["" for _ in range(columns)] for _ in range(rows)]
    for cell in cells:
        if cell["isHeader"]:
            headers[cell["Coordinates"]["column"]] = cell["cleanedText"]
        else:
            row = cell["Coordinates"]["row"] - 1
            column = cell["Coordinates"]["column"]
            text = cell["cleanedText"]
            # Rimozione di pattern specifici dal testo
            pattern = r"\d{2}x\d{2}px"
            text = re.sub(pattern, '', text)
            text = text.strip()
            table_data[row][column] = text  
    table_dataframe = pd.DataFrame(table_data, columns=headers)
    tables[table_name] = table_dataframe

# Lettura del file JSON del risultato finale e ridimensionamento
final_table_path = os.path.join(ABS_PATH, "processed-final-table2.json")
final_table = pd.read_json(final_table_path)
final_table = final_table.iloc[:200]
# Rinomina di una colonna nel DataFrame finale
final_table.rename(columns={'country': 'country_headquarters'}, inplace=True)

# Percorso del file contenente le corrispondenze tra colonne
MATCHES_PATH = os.path.join(ABS_PATH, "matches")
# Caricamento delle corrispondenze se il file esiste, altrimenti creazione di nuove corrispondenze
if os.path.exists(MATCHES_PATH):
    with open(MATCHES_PATH, 'rb') as pickle_file:
        matches = pickle.load(pickle_file)
else:
    matcher = Coma(use_instances=True, java_xmx="2048m")
    matches = {}
    for i, table_name in enumerate(tables):
        table = tables[table_name]
        print(f"Matching {i} - {table_name}")
        result = valentine_match(final_table, table.iloc[:200], matcher)
        for key in result:
            score = result[key]
            key = (("final-table", key[0][1]), (table_name, key[1][1]))
            matches[key] = score    
    with open(MATCHES_PATH, "wb") as file:
        pickle.dump(matches, file)

# Identificazione delle tabelle candidate per le corrispondenze
candidate_tables = set()
for match in matches:
    score = matches[match]
    if match[0][1] == "company_name" and score > 0.3:
        table_name = match[1][0]
        candidate_tables.add(table_name)
print(f"Number of candidate tables: {len(candidate_tables)}")

# Elaborazione delle corrispondenze rilevate
processed_matches = {}
for match in matches:
    table_name = match[1][0]
    if table_name not in candidate_tables:
        continue
    score = matches[match]
    if score < 0.3:
        continue
    original_column = match[0][1]
    to_column = match[1][1]
    if table_name not in processed_matches:
        processed_matches[table_name] = [(original_column, to_column, score)]
    else:
        processed_matches[table_name].append((original_column, to_column, score))

# Rinominazione delle colonne delle tabelle candidate
for table_name in processed_matches:
    print(table_name)
    print(processed_matches[table_name])
    print()

header_final_table = final_table.columns.tolist()
print()

# Creazione della directory di output
OUTPUT_PATH = os.path.join(ABS_PATH, "output")
if os.path.exists(OUTPUT_PATH):
    shutil.rmtree(OUTPUT_PATH)
os.mkdir(OUTPUT_PATH)

print(len(processed_matches))

total_new_entries = 0
for number, table_name in enumerate(processed_matches):
    table = tables[table_name]
    old_header = table.columns.tolist()
    print(table_name)
    print("Old header:", old_header)
    new_header = table.columns.tolist()
    for i, column_name in enumerate(old_header):
        for original_column, to_column, _ in processed_matches[table_name]:
            if to_column == column_name:
                new_header[i] = original_column
    if "country_headquarters" in new_header:
        position = new_header.index("country_headquarters")
        new_header[position] = "country"
    print("New header:", new_header)
    print("\nGood matches:")
    for column_name in old_header:
        for match in matches:
            score = matches[match]
            if match[1] == (table_name, column_name) and score > 0.3 and match[0][1] != "company_name":
                print(match[0][1], " - ", match[1][1], score)
    table.columns = new_header
    print()
    print(table.iloc[:5])
    table_path = os.path.join(OUTPUT_PATH, str(number) + '.json')
    print("Table path:", table_path)
    table.to_json(table_path, orient='records', indent=4)
    print("\n\n\n")
    total_new_entries += len(table)

print(f"Total new entries: {total_new_entries}")
print()
print(f"Old mediated schema: {len(header_final_table)}")
print(header_final_table)
print()
print(f"New mediated schema: {len(new_header)}")
print(new_header)
