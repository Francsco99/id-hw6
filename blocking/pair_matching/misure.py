import pandas as pd

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
#df=pd.DataFrame({'company_name':['negro','ciao','pluto','pippo','ci ao','ciao ',' pippo '],"country":['italia','spagna','uk','us','filippine','romania','germania']})
# Trasforma tutte le stringhe del DataFrame in minuscolo
df = df.map(lambda x: x.lower() if isinstance(x, str) else x)
df['company_name'] = df['company_name'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in company_forms_separated_lowercase]))

print(df.head())

dizionario_conta={}
dizionario_completo={}

# Scorrere riga per riga
for index, row in df.iterrows():
    nome = row["company_name"]
    if nome in dizionario_conta:
        dizionario_conta[nome] +=1
        dizionario_completo[nome].append(row)
    else:
        dizionario_conta[nome]=1
        dizionario_completo[nome]=[row]

totali = 0
for k,v in dizionario_conta.items():
    totali +=v
true_negative = len(dizionario_conta)
true_positive = totali-true_negative
false_positive=true_negative
false_negative=true_positive

#TP/(TP+FP)
precision=true_positive/(true_positive+false_positive)

#TP/(TP+FN)
recall = true_positive/(true_positive+false_negative)

#(TP+TN)/(TP+FP+TN+FN)
accuracy =(true_positive+true_negative)/(true_positive+false_positive+true_negative+false_negative)

print("totale entry: ",totali)
print("true positive: ",true_positive)
print("true negative: ",true_negative)
print("precision: ",precision)
print("recall: ",recall)
print("accuracy: ",accuracy)
