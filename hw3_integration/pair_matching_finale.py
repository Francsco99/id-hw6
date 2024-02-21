import pandas as pd
import recordlinkage
import recordlinkage.preprocessing
import time
import os
import re
from recordlinkage.base import BaseCompareFeature
from recordlinkage.base import BaseIndexAlgorithm
import Levenshtein

# Percorsi delle cartelle di input e output
absPath = os.path.dirname(os.path.abspath(__file__))
TABELLA_FINALE = '/Users/fspezzano/vscode/id-hw6/hw3_integration/json/final_table-hw3_alinged-last.json'
OUTPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/hw3_integration/json/paired.json'

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

class FirstTwoLettersIndex(BaseIndexAlgorithm):
    """Custom class for indexing based on the first two letters of given names."""

    def _link_index(self, df_a, df_b):
        """Make pairs with given names starting with the same first two letters."""

        # Create a temporary column to store the first two letters of given names
        df_a['first_two_letters'] = df_a['company_name'].str[:2]
        df_b['first_two_letters'] = df_b['company_name'].str[:2]

        # Find unique combinations of the first two letters present in both dataframes
        common_first_two_letters = set(df_a['first_two_letters']).intersection(df_b['first_two_letters'])

        # Initialize an empty list to store the index pairs
        index_pairs = []

        # For each common first two letters, find matching records and add their index pairs to the list
        for letters in common_first_two_letters:
            name_a_indices = df_a[df_a['first_two_letters'] == letters].index
            name_b_indices = df_b[df_b['first_two_letters'] == letters].index
            index_pairs.extend([(a, b) for a in name_a_indices for b in name_b_indices])

        # Remove the temporary columns
        df_a.drop(columns=['first_two_letters'], inplace=True)
        #df_b.drop(columns=['first_two_letters'], inplace=True)

        # Convert the list of pairs to a MultiIndex
        return pd.MultiIndex.from_tuples(index_pairs, names=[df_a.index.name, df_b.index.name])


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
conteggio=0
match_totali=0

# Creazione di un indice per le coppie candidate
indexer = FirstTwoLettersIndex()

# Comparazione delle coppie candidate basata attrributo company_name
compare = recordlinkage.Compare()
compare.add(CompareCompanyName('company_name','company_name'))

# Caricamento del DataFrame dal file JSON
tabella_finale = pd.read_json(TABELLA_FINALE)

candidate_links = indexer.index(tabella_finale)

# Calcolo dei punteggi di similarità
features = compare.compute(candidate_links, tabella_finale)

# Selezione delle coppie con punteggi alti (esempio: somma dei punteggi > soglia)
matches = features[features.sum(axis=1) > 0.7]  # Soglia da adattare
match_totali +=len(matches)
        
# Unificazione delle coppie e rimozione dei duplicati
df_unified = unify_matches(tabella_finale, matches)
        
# Salva la stringa JSON in un file
saveFile(df_unified,OUTPUT_FOLDER)
print("Tempo totale:", time.time() - start_time)
print("Match totali controllati: ",match_totali)
