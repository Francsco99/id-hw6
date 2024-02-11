import os
import json

def readJsonFile(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data

def saveJsonFile(data, output_file):
    with open(output_file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)

# Supponendo che ABS_PATH e INPUT_FOLDER siano definiti come nel tuo script
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(ABS_PATH, "unified_final_table_new.json")
OUTPUT_FOLDER = os.path.join(ABS_PATH, "output") # Modificato per includere una sottocartella "output"

data = readJsonFile(INPUT_FOLDER)
i=0

#for element in data:
    #if element["trade_name"]:
        #i+=1
        #print(f"company name: {element["company_name"]}, trade name: {element["trade_name"]}")
#print(i)

i=0
for element in data:
    i+=1
print(i)