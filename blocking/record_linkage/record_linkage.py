import recordlinkage as rl
import pandas as pd

# Leggi il DataFrame
df = pd.read_json('/Users/fspezzano/vscode/id-hw6/blocking/final_table_new.json')

# Definisci un indice
indexer = rl.Index()
indexer.block('company_name')  # Usa il blocco sul nome della compagnia come indice

# Trova i collegamenti candidati
candidate_links = indexer.index(df)

# Specifica le colonne da confrontare
comp = rl.Compare()
comp.string('company_name', 'company_name', method='levenshtein')

# Calcola i punteggi di comparazione
features = comp.compute(candidate_links, df)


'''
# Stampa solo i primi 10 record corrispondenti
for i, record_pair in enumerate(linked_records):
   
    
    index1, index2 = record_pair
    record1 = df.loc[index1]
    record2 = df.loc[index2]
    print("Record 1:\n", record1["company_name"])
    print("Record 2:\n", record2["company_name"])
    print("\n")
'''