import pandas as pd
import recordlinkage
import recordlinkage.preprocessing
import time

# Lista di valori per la colonna "company_name"
company_names = ["BAD APPLE CIDER", "BAD APPLE"]
industries = ["59200 - Sound recording and music publishing activities","11030 - Manufacture of cider and other fruit wines"]
# Creazione del DataFrame
df = pd.DataFrame({'company_name': company_names,'industry':industries})
# Trasforma tutte le stringhe del DataFrame in minuscolo
df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
print(df)
# Creazione di un indice per le coppie candidate
indexer = recordlinkage.Index()

indexer.full()  # Sostituire con il campo chiave appropriato
candidate_links = indexer.index(df)
tempo_candidate_links = time.time()

print(candidate_links)

# Comparazione delle coppie candidate basata su più attributi
compare = recordlinkage.Compare()

compare.string('company_name', 'company_name', method='cosine')
compare.string('industry','industry',method='cosine',missing_value=0.1)

#compare.string('location_city','location_city',method='jarowinkler',missing_value=0.2)
features = compare.compute(candidate_links, df)
print(features)