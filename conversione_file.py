# Importazione dei moduli necessari per la manipolazione dei dati e l'interazione con il sistema di file
import os
import json
import pandas as pd
import shutil

# Definisce una funzione per leggere un file JSON e restituire il suo contenuto.
def read_json_file(file_path):
    # Apre il file in modalità lettura ('r') e carica il suo contenuto come un oggetto Python
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

# Definisce una funzione per convertire dati Python in formato JSON e salvarli in un file.
def convert_to_json(data, json_file_path):
    # Apre il file di destinazione in modalità scrittura ('w') e scrive i dati in formato JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Definisce una funzione per convertire file CSV o Excel in JSON.
def file_to_json(file_path, json_file_path, file_type):
    # Gestisce i file CSV
    if file_type == 'csv':
        try:
            # Tenta di leggere il file CSV con encoding UTF-8
            data = pd.read_csv(file_path, encoding='utf-8').to_dict(orient='records')
        except UnicodeDecodeError:
            # Se si verifica un errore di codifica, prova con ISO-8859-1
            data = pd.read_csv(file_path, encoding='iso-8859-1').to_dict(orient='records')
    # Gestisce i file Excel (xls e xlsx)
    elif file_type in ['xls', 'xlsx']:
        data = pd.read_excel(file_path).to_dict(orient='records')
    # Converte i dati in JSON e li salva nel percorso specificato
    convert_to_json(data, json_file_path)

# Prepara la directory di destinazione per i file JSON.
destination_dir = "sources_json"
# Controlla se la directory esiste già e, in caso affermativo, la elimina per evitare duplicati
if os.path.exists(destination_dir):
    shutil.rmtree(destination_dir)
# Crea una nuova directory vuota
os.mkdir(destination_dir)

# Imposta la directory sorgente da cui leggere i file originali
source_dir = "sources"

# Itera su tutti i file presenti nella directory sorgente
for file_name in os.listdir(source_dir):
    # Costruisce il percorso completo del file originale
    origin_path = os.path.join(source_dir, file_name)
    # Estrae l'estensione del file per determinarne il tipo
    file_extension = file_name.split('.')[-1]
    # Definisce il percorso del file di destinazione, cambiando l'estensione in .json
    destination_path = os.path.join(destination_dir, file_name.rsplit('.', 1)[0] + ".json")

    # Gestisce la conversione in base al tipo di file
    if file_extension in ['json', 'jsonl']:
        # Per i file JSON, legge e riscrive semplicemente i dati
        if file_extension == 'json':
            data = read_json_file(origin_path)
        else:  # Per i file JSONL, legge ogni linea come un oggetto JSON separato
            with open(origin_path, 'r') as jsonl_file:
                data = [json.loads(line) for line in jsonl_file]
        # Converte i dati in formato JSON e li salva
        convert_to_json(data, destination_path)
    elif file_extension in ['csv', 'xls', 'xlsx']:
        # Utilizza la funzione definita per convertire CSV e Excel in JSON
        file_to_json(origin_path, destination_path, file_extension)
    else:
        # Se il tipo di file non è supportato, stampa un messaggio
        print(f"Skipping unsupported file type: {file_name}")
