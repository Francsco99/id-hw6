import os
import json

def combine_json_files(input_folder, output_file):
    combined_data = []

    # Elenco di tutti i file nella directory specificata
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.json'):
            # Costruisce il percorso completo al file
            file_path = os.path.join(input_folder, file_name)
            # Apre e legge il contenuto del file JSON
            with open(file_path, 'r') as file:
                data = json.load(file)
                combined_data.extend(data)  # Aggiunge i dati alla lista complessiva

    # Scrive i dati combinati in un nuovo file JSON
    with open(output_file, 'w') as output_file:
        json.dump(combined_data, output_file, indent=4)

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/pairwise_matching/json/country'
OUTPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/pairwise_matching/json/final_table_country.json'

combine_json_files(INPUT_FOLDER, OUTPUT_FOLDER)
