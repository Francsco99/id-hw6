import pandas as pd
import recordlinkage
import recordlinkage.preprocessing

# Caricamento del DataFrame dal file JSON
df = pd.read_json('/Users/fspezzano/vscode/id-hw6/blocking/final_table_new.json')


# Lista delle sigle da rimuovere
company_forms_separated_lowercase = [
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

# Trasforma tutte le stringhe del DataFrame in minuscolo
df = df.map(lambda x: x.lower() if isinstance(x, str) else x)
df['company_name'] = df['company_name'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in company_forms_separated_lowercase]))

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
matches = features[features.sum(axis=1) > 1.3]  # Soglia da adattare
linked_records = matches.index

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

# Salvataggio del DataFrame unificato
# Converti il DataFrame in una stringa JSON con indentazione
json_str = df_unified.to_json(orient='records', indent=4)

# Salva la stringa JSON in un file
with open('/Users/fspezzano/vscode/id-hw6/blocking/pairwise_output_company_name.json', 'w') as f:
    f.write(json_str)