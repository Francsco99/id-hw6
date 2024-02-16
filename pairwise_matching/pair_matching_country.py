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
INPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/blocking/json/country_blocks'
OUTPUT_FOLDER = os.path.join(absPath,'json/country')

start_time = time.time()

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

# Elenco dei file nella cartella di input
input_files = os.listdir(INPUT_FOLDER)
num_files = len(input_files)
conteggio=0
match_totali=0
# Creazione di un indice per le coppie candidate
indexer = recordlinkage.Index()
indexer.block("country") 

# Comparazione delle coppie candidate basata su più attributi
compare = recordlinkage.Compare()

compare.string('country','country',method='cosine')
compare.string('company_name', 'company_name', method='cosine')
compare.string('industry','industry',method='cosine',missing_value=0.1)

for input_file in input_files:
    conteggio+=1
    print("FILE CORRENTE ",input_file)

    input_path = os.path.join(INPUT_FOLDER, input_file)
    output_file = os.path.join(OUTPUT_FOLDER, input_file.replace('.json', '-proc.json'))
    
    # Caricamento del DataFrame dal file JSON
    df = pd.read_json(input_path)

    df['company_name'] = df['company_name'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in COMPANY_SIGLE]))

    # Controllo se il DataFrame è vuoto
    if df.empty:
        saveFile(df,output_file)
        print(f"{input_file} è vuoto, copiato in output.")
        continue

    '''# Controllo se tutti i valori del DataFrame sono stop word
    if df.map(lambda x: isinstance(x, str) and x.isspace()).all().all():
        saveFile(df,output_file)
        print(f"{input_file} contiene solo stop word, copiato in output")
        continue'''
    
    # Controllo se il file ha una sola entry
    if len(df) == 1:
        saveFile(df,output_file)
        print(f"{input_file} contiene una sola entry.")
        continue

    candidate_links = indexer.index(df)

    # Calcolo dei punteggi di similarità
    features = compare.compute(candidate_links, df)

    # Selezione delle coppie con punteggi alti (esempio: somma dei punteggi > soglia)
    matches = features[features.sum(axis=1) > 1.7]  # Soglia da adattare
    match_totali +=len(matches)
    # Unificazione delle coppie e rimozione dei duplicati
    df_unified = unify_matches(df, matches)

    # Salva la stringa JSON in un file
    saveFile(df_unified,output_file)
    print(f"Processato {input_file}.json ({len(matches)} match controllati)\t file {conteggio} di {num_files}")

print("Tempo totale:", time.time() - start_time)
print("Match totali controllati: ",match_totali)
