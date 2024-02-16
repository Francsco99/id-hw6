
import pandas as pd
import unicodedata as uc
import re
INPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/final_table_new.json'
OUTPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/final_table_lower_normalized.json'

'''def normalize_text(stringa):
    #pulisci = uc.normalize('NFKD', stringa).encode('ascii', 'ignore').decode('utf-8')
    name_pulito = re.sub(r'[^a-zA-Z0-9]', '', stringa)
    return name_pulito'''

# Caricamento del DataFrame dal file JSON
df = pd.read_json(INPUT_FOLDER)

# Trasforma tutte le stringhe del DataFrame in minuscolo
df = df.map(lambda x: x.lower() if isinstance(x, str) else x)
#df['company_name']=df['company_name'].apply(normalize_text)
# Converti il DataFrame in una stringa JSON con indentazione
json_str = df.to_json(orient='records', indent=4)

# Salva la stringa JSON in un file
with open(OUTPUT_FOLDER, 'w') as f:
    f.write(json_str)
