import pandas as pd
import recordlinkage
import recordlinkage.preprocessing

# Caricamento del DataFrame dal file JSON
df = pd.read_json('/Users/fspezzano/vscode/id-hw6/blocking/test.json')

# Trasforma tutte le stringhe del DataFrame in minuscolo
df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

# Creazione di un indice per le coppie candidate
indexer = recordlinkage.Index()
indexer.block('company_name')  # Sostituire con il campo chiave appropriato
candidate_links = indexer.index(df)

# Comparazione delle coppie candidate basata su più attributi
compare = recordlinkage.Compare()
compare.string('company_name', 'company_name', method='jarowinkler', threshold=0.85)
compare.string('country', 'country', method='jarowinkler', threshold=0.85)
# Aggiungi altre comparazioni se necessario

# Calcolo dei punteggi di similarità
features = compare.compute(candidate_links, df)

# Selezione delle coppie con punteggi alti (esempio: somma dei punteggi > soglia)
matches = features[features.sum(axis=1) > 0.5]  # Soglia da adattare
linked_records = matches.index
'''
for i, record_pair in enumerate(linked_records):
    index1, index2 = record_pair
    record1 = df.loc[index1]
    record2 = df.loc[index2]
    print("Record 1:\n", record1["company_code"])
    print("Record 2:\n", record2["company_code"])
    print("\n")
'''

# Unificazione dei record basata sui match trovati
def unify_matches(df, matches):
    for index_pair in matches.index:
        record1 = df.loc[index_pair[0]]
        record2 = df.loc[index_pair[1]]

        # Unione dei record
        for col in df.columns:
            print(col)
            if pd.isna(record1[col]) and not pd.isna(record2[col]):
                df.at[index_pair[0], col] = record2[col]
                print("ciao")
                print( df.at[index_pair[0], col])
            elif pd.isna(record2[col]) and not pd.isna(record1[col]):
                print("sono")
                df.at[index_pair[1], col] = record1[col]
            elif pd.isna(record1[col]) and pd.isna(record2[col]):
                print("qui")
                continue  # Se entrambi i valori sono mancanti, non fare nulla
                
    # Rimuovere i record duplicati dopo l'unificazione
    df = df.drop_duplicates()
    return df

df_unified = unify_matches(df, matches)

# Salvataggio del DataFrame unificato
# Converti il DataFrame in una stringa JSON con indentazione
json_str = df_unified.to_json(orient='records', indent=4)

# Salva la stringa JSON in un file
with open('/Users/fspezzano/vscode/id-hw6/blocking/unified_final_table_new.json', 'w') as f:
    f.write(json_str)