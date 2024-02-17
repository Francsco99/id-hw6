import pandas as pd
import recordlinkage
import recordlinkage.preprocessing
import time
import os
import re
from recordlinkage.base import BaseCompareFeature
import Levenshtein
import numpy

# Percorsi delle cartelle di input e output
absPath = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/blocking/json/country_blocks'
OUTPUT_FOLDER = os.path.join(absPath,'json/country')
class CompareCompanyName(BaseCompareFeature):
    def _compute_vectorized(self, s1,s2):
        def normalize_text(stringa):
            return re.sub(r'[^a-zA-Z0-9]', '', stringa)
        
        s1_norm = s1.map(normalize_text)
        s2_norm = s2.map(normalize_text)

        def norm_lev_dist(str1,str2):
            dist = Levenshtein.distance(str1,str2)
            max_len = max(len(str1),len(str2))
            if max_len == 0:
                return 0
            return 1-(dist/max_len)
        vectoriz_dist = s1_norm.combine(s2_norm,norm_lev_dist)
    
        return vectoriz_dist

def is_json_file(filename):
    _, file_extension = os.path.splitext(filename)
    return file_extension.lower() == '.json'

def piuLungo(val1,val2):
    if len(str(val1))> len(str(val2)):
        return val1
    return val2

def unify_matches(df, matches):
    for index_pair in matches.index:
        record1 = df.loc[index_pair[0]]
        record2 = df.loc[index_pair[1]]
        # Unione dei record
        for col in df.columns:
            # Se il primo valore è mancante e il secondo è presente
            if pd.isna(record1[col]) or record1[col] == "":
                if not pd.isna(record2[col]) and record2[col] != "":
                    df.at[index_pair[0], col] = record2[col]
            # Se il secondo valore è mancante e il primo è presente
            elif pd.isna(record2[col]) or record2[col] == "":
                df.at[index_pair[1], col] = record1[col]
            # Se entrambi i valori sono presenti
            else:
                nuovo_valore = piuLungo(record1[col], record2[col])
                df.at[index_pair[0], col] = nuovo_valore
                df.at[index_pair[1], col] = nuovo_valore

    # Rimuovere i record duplicati dopo l'unificazione
    df = df.drop_duplicates()
    return df

def saveFile(df,out_path):
    out_df = df.to_json(orient='records', indent=4)
    with open(out_path, 'w') as f:
        f.write(out_df)

start_time = time.time()
# Elenco dei file nella cartella di input
input_files = os.listdir(INPUT_FOLDER)
num_files = len(input_files)
conteggio=0
match_totali=0

# Creazione di un indice per le coppie candidate
indexer = recordlinkage.Index()
indexer.full()

# Comparazione delle coppie candidate basata attrributo company_name
compare = recordlinkage.Compare()
compare.add(CompareCompanyName('company_name','company_name'))

for input_file in input_files:
    if is_json_file(input_file): 
        conteggio+=1
        print("FILE CORRENTE ",input_file)

        input_path = os.path.join(INPUT_FOLDER, input_file)
        output_file = os.path.join(OUTPUT_FOLDER, input_file.replace('.json', '-proc.json'))
        
        # Caricamento del DataFrame dal file JSON
        df = pd.read_json(input_path)
        
        # Controllo se il DataFrame è vuoto
        if df.empty:
            saveFile(df,output_file)
            print(f"{input_file} è vuoto, copiato in output.")
            continue
        
        # Controllo se il file ha una sola entry
        if len(df) == 1:
            saveFile(df,output_file)
            print(f"{input_file} contiene una sola entry.")
            continue
        
        candidate_links = indexer.index(df)

        # Calcolo dei punteggi di similarità
        features = compare.compute(candidate_links, df)

        # Selezione delle coppie con punteggi alti (esempio: somma dei punteggi > soglia)
        matches = features[features.sum(axis=1) > 0.7]  # Soglia da adattare
        match_totali +=len(matches)
        
        # Unificazione delle coppie e rimozione dei duplicati
        df_unified = unify_matches(df, matches)
        
        # Salva la stringa JSON in un file
        saveFile(df_unified,output_file)
        print(f"Processato {input_file} ({len(matches)} match controllati)\t file {conteggio} di {num_files}")

print("Tempo totale:", time.time() - start_time)
print("Match totali controllati: ",match_totali)
