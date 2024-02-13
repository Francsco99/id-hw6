import pandas as pd
import recordlinkage
import recordlinkage.preprocessing
import time

start_time = time.time()
# Caricamento del DataFrame dal file JSON
df = pd.read_json('/Users/fspezzano/vscode/id-hw6/blocking/output/block-paesi/test_country.json')

# Trasforma tutte le stringhe del DataFrame in minuscolo
df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
tempo_lower_case = time.time()
print("Tempo per mettere lowercase: ",tempo_lower_case-start_time)

# Creazione di un indice per le coppie candidate
indexer = recordlinkage.Index()

indexer.full()  # Sostituire con il campo chiave appropriato
tempo_index_full=time.time()
print("Tempo per index full: ",tempo_index_full-tempo_lower_case)
#indexer.block('country')
tempo_index_block=time.time()
#print("Tempo per index block: ",tempo_index_block-start_time)
candidate_links = indexer.index(df)
tempo_candidate_links = time.time()
print("Tempo per creare coppie candidate: ",tempo_candidate_links-tempo_index_full)
print(len(candidate_links))
# Comparazione delle coppie candidate basata su più attributi
compare = recordlinkage.Compare()

compare.string('company_name', 'company_name', method='jarowinkler')
compare.string('industry','industry',method='jarowinkler',missing_value=0.2)
compare.string('location_city','location_city',method='jarowinkler',missing_value=0.2)

tempo_comparazione_coppie = time.time()
print("Tempo per comparazione coppie: ",tempo_comparazione_coppie-tempo_candidate_links)

# Calcolo dei punteggi di similarità
features = compare.compute(candidate_links, df)
tempo_calcolo_punteggi = time.time()
print("Tempo per calcolare i punteggi: ",tempo_calcolo_punteggi-tempo_comparazione_coppie)
print(len(features))

# Selezione delle coppie con punteggi alti (esempio: somma dei punteggi > soglia)
print(features[features.sum(axis=1)])
matches = features[features.sum(axis=1) > 1.7]  # Soglia da adattare

print(len(matches))

#matches = features
tempo_selezione_link = time.time()
print("Tempo per selezione link: ",tempo_selezione_link-tempo_calcolo_punteggi)

"""
for i, record_pair in enumerate(linked_records):
    print("match: ", i+1)
    index1, index2 = record_pair
    record1 = df.loc[index1]
    record2 = df.loc[index2]
    print("Record 1:\n", record1["company_code"])
    print("Record 2:\n", record2["company_code"])
    print("\n")
print("\n")
print("\n")
print("\n")
print("\n") 
"""

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


df_unified = unify_matches(df, matches)

tempo_unifica_elima_doppi = time.time()
print("Tempo per eliminazione doppi e unifica: ",tempo_unifica_elima_doppi-tempo_selezione_link)
# Salvataggio del DataFrame unificato
# Converti il DataFrame in una stringa JSON con indentazione
json_str = df_unified.to_json(orient='records', indent=4)

# Salva la stringa JSON in un file
with open('/Users/fspezzano/vscode/id-hw6/blocking/pairwise_country/test-proc.json', 'w') as f:
    f.write(json_str)