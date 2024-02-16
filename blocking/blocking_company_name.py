import json
import os
import re

def readJsonFile(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data

def saveJsonFile(data, output_file):
    with open(output_file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)

def removeCompanyForm(company_name, company_forms):
    # Aggiunta di pattern specifici per ", ", " ,", "; ", " ;" oltre agli spazi, virgole e punto e virgola standard
    pattern = r'[\s;,-]*\s*(?:,?\s*;?\s*-?\s*)*(?:' + '|'.join(re.escape(form) for form in company_forms) + r')\s*$'
    # Rimozione della sigla e dei caratteri precedenti specificati
    new_name = re.sub(pattern, '', company_name, flags=re.IGNORECASE)
    return new_name

def searchCompanyName(element, initial, company_names):
    if initial in company_names:
        company_names[initial].append(element)
    else:
        company_names[initial] = [element]

def organizeByCompanyName(data, company_forms):
    company_names = {}
    for element in data:
        company_name = element.get("company_name", "")
        if company_name:  # Se il nome dell'azienda è presente
            cleaned_name = removeCompanyForm(company_name, company_forms)
            initial = cleaned_name.upper()  # Converti la stringa pulita in maiuscolo
            searchCompanyName(element, initial, company_names)
        else:
            # Gestione dei casi in cui il nome dell'azienda non è disponibile
            searchCompanyName(element, "Unknown", company_names)
    return company_names

# ABS_PATH e INPUT_FOLDER definiti 
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(ABS_PATH, "fixed_total.json")
OUTPUT_FOLDER = os.path.join(ABS_PATH, "output")

# Assicurati che la cartella di output esista
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Definizione delle sigle da rimuovere
company_forms_separated_uppercase = [
    "S.P.A.", "SOCIETA PER AZIONI", "SPA", "S.P.A", "& CO", "SPA LIMITED", "AND SPA LIMITED", "AND SPA LTD", "SPA LTD", "& SPA LTD", "& SPA LIMITED",
    "S.R.L.", "SRL", "& SPA",
    "INC.", "INCORPORATED", "CORPORATION LIMITED", "LIMITED", "CORPORATION", "UNLIMITED CORP.", "CORP.", "CORP", "UNLIMITED",
    "INC.", "L.L.C", "L.L.C.", "L.L.C.", "THE", "INC", "INC UK LIMITED",
    "LLC", "LIMITED LIABILITY COMPANY", "GMBH", "GESELLSCHAFT MIT BESCHRÄNKTER HAFTUNG", "PUBLIC COMPANY LTD",
    "AG", "A.G.", "AKTIENGESELLSCHAFT", "PUBLIC COMPANY", "LTD.", "LIMITED", "LTD", "LP", "L.P", "L.P.", "SOCIETE PAR ACTIONS SIMPLIFIEE",
    "SA", "SOCIETE ANONYME", "S.A", "S.A.", "& SPA LIMITED", "TBK.",
    "BV", "BESLOTEN VENNOOTSCHAP", "PLC", "TBK", "A.S", "T.A.S.", "AS", "A.S.", "A-S", "OYJ", "OY", "CAREERS", "CO.", "COMPANY", "CO", "CO.,LTD", "CO., LTD.", "CO.,LTD.",
    "CO. LTD", "GES.M.B.H.", "M.B.H.", "GMBH","LLC CAREERS", "LLP CAREERS", "LTD. CAREERS","INC. CAREERS","& CO CAREERS", " "
]


# Supponi che il resto del setup per ABS_PATH, INPUT_FOLDER e OUTPUT_FOLDER sia già definito qui

data = readJsonFile(INPUT_FOLDER)
company_names = organizeByCompanyName(data, company_forms_separated_uppercase)
print(company_names.keys())
print("Elementi nel dizionario: ", len(company_names))

# Salvataggio del file JSON
output_file_path = os.path.join(OUTPUT_FOLDER, "company_names.json")
saveJsonFile(company_names, output_file_path)
