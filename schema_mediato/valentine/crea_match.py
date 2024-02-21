import os
import pickle
from multiprocessing import Process
from time import time
from valentine import valentine_match
from valentine.algorithms import Coma
import pandas as pd
import shutil

# Ottieni il percorso assoluto della directory corrente
absPath = os.path.dirname(os.path.abspath(__file__))
MATCHES_DIRECTORY = absPath + "/matches-hw3"

# Funzione per analizzare un chunk di confronti tra schemi
def parseChunk(chunk, schemaList, schemaNames, processNumber):
    # Inizializza l'algoritmo di confronto
    matcher = Coma(use_instances=True, java_xmx="4096m")
    matches = dict()  # Dizionario per memorizzare i match tra attributi
    n = 0  # Contatore per il numero di confronti
    for comparison in chunk:
        n += 1
        print(n)
        i = comparison[0]  # Indice del primo schema nel confronto
        j = comparison[1]  # Indice del secondo schema nel confronto
        # Esegue il confronto tra gli schemi e memorizza i risultati nei match
        result = valentine_match(schemaList[i], schemaList[j], matcher, schemaNames[i], schemaNames[j])
        for key in result:
            score = result[key]
            matches[key] = score
    print(f"finished {processNumber} process")
    # Salva i match in un file pickle
    pickle.dump(matches, open(MATCHES_DIRECTORY + "/matches-hw3" + str(processNumber), 'wb'))

if __name__ == "__main__":
    start = time()  # Registra il tempo di inizio
    numProcs = 2  # Numero di processi paralleli
    procs = []  # Lista per memorizzare i processi
    parsers = []  # Lista per memorizzare i parser
    dataSource = '/Users/fspezzano/vscode/id-hw6/hw3_integration/json/tabelle_da_unire'  # Directory dei dati sorgente
    files = os.listdir(dataSource)  # Ottieni la lista dei file JSON
    schemaList = []  # Lista per memorizzare gli schemi
    schemaNames = []  # Lista per memorizzare i nomi degli schemi
    # Carica i dati da ciascun file JSON nella lista degli schemi
    for file in files:
        filePath = dataSource + "/" + file
        df = pd.read_json(filePath)
        df = df.iloc[:500]  # Limita il numero di righe per efficienza
        schemaList.append(df)
        schemaNames.append(file)
    totalSchemas = len(schemaList)  # Numero totale di schemi
    totalComparisons = totalSchemas * (totalSchemas - 1) // 2  # Numero totale di confronti
    comparisons = []  # Lista per memorizzare i confronti tra gli schemi
    chunk_size = totalComparisons // numProcs  # Dimensione di ciascun chunk
    remainder = totalComparisons - chunk_size * numProcs  # Resto dei confronti
    # Genera tutti i possibili confronti tra gli schemi
    for i in range(totalSchemas - 1):
        for j in range(i + 1, totalSchemas):
            comparisons.append((i, j))
    # Dividi i confronti in chunk per la parallelizzazione
    chunks = [comparisons[i: i + chunk_size] for i in range(0, len(comparisons) - remainder, chunk_size)]
    # Distribuisci i restanti confronti tra i chunk esistenti
    if remainder != 0:
        for i, elem in enumerate(comparisons[-remainder:]):
            chunks[i].append(elem)
    # Rimuovi la directory dei match se esiste già e crea una nuova directory
    if os.path.exists(MATCHES_DIRECTORY):
        shutil.rmtree(MATCHES_DIRECTORY)
    os.mkdir(MATCHES_DIRECTORY)
    try:
        # Avvia i processi per eseguire l'analisi dei chunk
        for i in range(numProcs):
            proc = Process(target=parseChunk, args=(chunks[i], schemaList, schemaNames, i))
            procs.append(proc)
            proc.start()
        # Attendi il completamento di tutti i processi
        for proc in procs:
            proc.join()
        # Calcola e stampa il tempo totale impiegato
        totalTime = str(time() - start)
        print(f"total time: {totalTime}")
    except KeyboardInterrupt:
        print("\nclosing all processes")
        # Interrompi tutti i processi se viene premuto Ctrl+C
        for proc in procs:
            proc.terminate()
        print("closed all processes")
