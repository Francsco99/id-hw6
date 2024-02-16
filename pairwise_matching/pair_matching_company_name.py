import pandas as pd
import recordlinkage
import recordlinkage.preprocessing
import time
import os

# Lista delle sigle da rimuovere
COMPANY_SIGLE = [
    "s.p.a.", "societa per azioni", "spa", "s.p.a", "& co", "spa limited", "and spa limited", "and spa ltd", "spa ltd", "& spa ltd", "& spa limited",
    "s.r.l.", "srl", "& spa",
    "inc.", "incorporated", "corporation limited", "limited", "corporation", "unlimited corp.", "corp.", "corp", "unlimited",
    "inc.", "l.l.c", "l.l.c.", "l.l.c.", "the", "inc", "inc uk limited",
    "llc", "limited liability company", "gmbh", "gesellschaft mit beschrankter haftung", "public company ltd",
    "ag", "a.g.", "aktiengesellschaft", "public company", "ltd.", "limited", "ltd", "lp", "l.p", "l.p.", "societe par actions simplifiee",
    "sa", "societe anonyme", "s.a", "s.a.", "& spa limited", "tbk.",
    "bv", "besloten vennootschap", "plc", "tbk", "a.s", "t.a.s.", "as", "a.s.", "a-s", "oyj", "oy", "careers", "co.", "company", "co", "co.,ltd", "co., ltd.", "co.,ltd.",
    "co. ltd", "ges.m.b.h.", "m.b.h.", "gmbh","llc careers", "llp careers", "ltd. careers","inc. careers","& co careers", " "
]

# Percorsi delle cartelle di input e output
absPath = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/final_table_lower.json'
OUTPUT_FOLDER = os.path.join(absPath,'json/final_table_company_name_sigle.json')

start_time = time.time()

# Caricamento del DataFrame dal file JSON
df = pd.read_json(INPUT_FOLDER)

#df['company_name'] = df['company_name'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in COMPANY_SIGLE]))
# Rimozione dei caratteri non alfanumerici dal campo 'company_name'
df['company_name'] = df['company_name'].str.replace(r'[^a-zA-Z0-9]', '')
tempo_lettura_json= time.time()

# Creazione di un indice per le coppie candidate
indexer = recordlinkage.Index()
indexer.block('company_name')  # Sostituire con il campo chiave appropriato
candidate_links = indexer.index(df)

# Comparazione delle coppie candidate basata su più attributi
compare = recordlinkage.Compare()

compare.string('country','country',method='cosine')
compare.string('company_name', 'company_name', method='cosine')
compare.string('industry','industry',method='cosine',missing_value=0.1)
#compare.string('location_city','location_city',method='cosine',missing_value=0.1)

# Calcolo dei punteggi di similarità
features = compare.compute(candidate_links, df)

# Selezione delle coppie con punteggi alti (esempio: somma dei punteggi > soglia)
matches = features[features.sum(axis=1) > 1]  # Soglia da adattare

tempo_creazione_coppie_candidate = time.time()

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

tempo_unione_coppie_rimozione_duplicati = time.time()

# Salvataggio del DataFrame unificato
# Converti il DataFrame in una stringa JSON con indentazione
json_str = df_unified.to_json(orient='records', indent=4)

# Salva la stringa JSON in un file
with open(OUTPUT_FOLDER, 'w') as f:
    f.write(json_str)

print("tempo lettura json: ",tempo_lettura_json-start_time)
print("tempo creazione coppie candidate: ",tempo_creazione_coppie_candidate-tempo_lettura_json)
print("tempo unione coppie e rimozione dupes",tempo_unione_coppie_rimozione_duplicati-tempo_creazione_coppie_candidate)
print("tempo_totale: ",time.time()-start_time)
print("match totali controllati: ",len(matches))