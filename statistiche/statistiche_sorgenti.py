import csv
import os
import json
import matplotlib.pyplot as plt


def salvare_dizionario_csv(dizionario, percorso_file_csv):
    # funzione per scrivere in un dizionario in un file CSV
    with open(percorso_file_csv, 'w', newline='') as file_csv:
        scrittore_csv = csv.DictWriter(file_csv, fieldnames=dizionario.keys())
    
        # Scrivi l'intestazione del file CSV
        scrittore_csv.writeheader()
    
        # Scrivi i dati del dizionario nel file CSV
        scrittore_csv.writerow(dizionario)


# Ottieni il percorso assoluto della directory corrente
absPath = os.path.dirname(os.path.abspath(__file__))
# Directory contenente i file JSON delle fonti
dataSource = '/Users/fspezzano/vscode/id-hw6/schema_mediato/valentine/sources_json'
dataOutput = os.path.join(absPath, "output")
files = os.listdir(dataSource)


# Inizializzazione delle variabili per le statistiche complessive
n_totale_righe_tutte_le_tabelle = 0
n_totale_colonne_tutte_le_tabelle = 0
n_totale_valori_nulli_tutte_le_tabelle = 0
max_righe = 0
nome_tabella_max_righe = ""
max_colonne = 0
nome_tabella_max_colonne = ""
max_valori_nulli = 0
nome_tabella_max_valori_nulli = ""
distribuzione_righe = {}
distribuzione_colonne = {}
distribuzione_righe_nomi={}
distribuzione_colonne_nomi={}
# Scansione dei file nella directory dei file JSON
for filename in files:
    if filename.endswith(".json"):
        file_path = os.path.join(dataSource, filename)
        with open(file_path, 'r') as f:
            data = json.load(f)

            # Variabili per la tabella corrente
            n_righe_tabella = 0
            n_colonne_tabella = 0
            elementi_nulli_tabella = 0

            # Scansione di ogni elemento nella tabella
            for element in data:
                n_righe_tabella += 1  # Conta righe di una tabella
                for k, v in element.items():
                    if not v or v == "" or v == " ":
                        elementi_nulli_tabella += 1

            # Calcolo delle statistiche per la tabella corrente
            n_colonne_tabella = len(data[0]) if data else 0  # Assume che la tabella abbia lo stesso numero di colonne
            n_totale_righe_tutte_le_tabelle += n_righe_tabella
            n_totale_colonne_tutte_le_tabelle += n_colonne_tabella
            n_totale_valori_nulli_tutte_le_tabelle += elementi_nulli_tabella

            # Aggiornamento della massima riga e massima colonna
            if n_righe_tabella > max_righe:
                max_righe = n_righe_tabella
                nome_tabella_max_righe = filename
            if n_colonne_tabella > max_colonne:
                max_colonne = n_colonne_tabella
                nome_tabella_max_colonne = filename

            # Aggiornamento della tabella con il massimo numero di valori nulli
            if elementi_nulli_tabella > max_valori_nulli:
                max_valori_nulli = elementi_nulli_tabella
                nome_tabella_max_valori_nulli = filename


            # distribuzione righe
            distribuzione_righe[n_righe_tabella] = distribuzione_righe.get(n_righe_tabella, 0) + 1

            # distribuzione colonne
            distribuzione_colonne[n_colonne_tabella] = distribuzione_colonne.get(n_colonne_tabella, 0) + 1

            #numero righe -> nome tabella
            if n_righe_tabella in distribuzione_righe_nomi:
                distribuzione_righe_nomi[n_righe_tabella].append(filename)
            else:
                distribuzione_righe_nomi[n_righe_tabella]=[]
                distribuzione_righe_nomi[n_righe_tabella].append(filename)
            
            #numero colonne -> nome tabella
            if n_colonne_tabella in distribuzione_colonne_nomi:
                distribuzione_colonne_nomi[n_colonne_tabella].append(filename)
            else:
                distribuzione_colonne_nomi[n_colonne_tabella]=[]
                distribuzione_colonne_nomi[n_colonne_tabella].append(filename)
# Calcolo delle medie per tabella
n_tabelle = len(files)
media_righe_x_tabella = n_totale_righe_tutte_le_tabelle / n_tabelle
media_colonne_x_tabella = n_totale_colonne_tutte_le_tabelle / n_tabelle
media_valori_nulli_x_tabella = n_totale_valori_nulli_tutte_le_tabelle / n_tabelle

distribuzione_righe_ordinata = dict(sorted(distribuzione_righe.items()))
distribuzione_colonne_ordinata = dict(sorted(distribuzione_colonne.items()))
distribuzione_righe_nomi_ordinata=dict(sorted(distribuzione_righe_nomi.items()))
distribuzione_colonne_nomi_ordinata=dict(sorted(distribuzione_colonne_nomi.items()))

# Stampa delle statistiche
print("Media righe x tabella:", media_righe_x_tabella)
print("Media colonne x tabella:", media_colonne_x_tabella)
print("Media valori nulli x tabella:", media_valori_nulli_x_tabella)
print("Max righe:", max_righe, "Nome tabella:", nome_tabella_max_righe)
print("Max colonne:", max_colonne, "Nome tabella:", nome_tabella_max_colonne)
print("Max valori nulli:", max_valori_nulli, "Nome tabella:", nome_tabella_max_valori_nulli)

# Stampa della distribuzione delle righe
print("Distribuzione righe:", distribuzione_righe_ordinata)

#print("Distribuzione colonne:", distribuzione_colonne)
print("Distribuzione colonne:", distribuzione_colonne_ordinata)

#print("Distribuzione colonne:", distribuzione_colonne)
#print("Distribuzione righe e nomi:", n_righe_nome_tabella)

# Salvataggio distribuzioni in file csv
salvare_dizionario_csv(distribuzione_colonne_ordinata, os.path.join(dataOutput, "distribuzione_colonne.csv"))
salvare_dizionario_csv(distribuzione_righe_ordinata, os.path.join(dataOutput, "distribuzione_righe.csv"))
salvare_dizionario_csv(distribuzione_righe_nomi,os.path.join(dataOutput,"righe_nomi.csv"))
salvare_dizionario_csv(distribuzione_colonne_nomi,os.path.join(dataOutput,"colonne_nomi.csv"))

def plot_distribution(data, title, xlabel, ylabel):
    if not data:
        print("No data available for plotting.")
        return
    
    keys = list(data.keys())
    values = list(data.values())
    
    plt.figure(figsize=(10, 6))  # Set figure background color
    plt.bar(range(len(keys)), values, color='#346c4e')  # Bar color
    plt.xlabel(xlabel, color='black')  # X-axis label color
    plt.ylabel(ylabel, color='black')  # Y-axis label color
    plt.title(title, color='black')  # Title color
    plt.xticks(range(len(keys)), keys, rotation=315, ha='center', color='black')  # X-axis tick labels color
    plt.yticks(color='black')  # Y-axis tick labels color
    plt.grid(axis='y', linestyle='dashed', color='gray')  # Grid color
    plt.tight_layout()  # Adjust layout to prevent overlap of labels
    plt.show()

# Plot distribution of columns
plot_distribution(distribuzione_colonne_ordinata, 'Distribuzione colonne', 'Numero di colonne', 'Numero di tabelle')

# Plot distribution of rows
print("Distribution of Rows:", distribuzione_righe_ordinata)
plot_distribution(distribuzione_righe_ordinata, 'Distribuzione righe', 'Numero di righe', 'Numero di tabelle')
