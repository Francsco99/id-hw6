import os
import json
import re

def readJsonFile(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data

def saveJsonFile(data, output_file):
    with open(output_file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)

# Supponendo che ABS_PATH e INPUT_FOLDER siano definiti come nel tuo script
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(ABS_PATH, "fixed_total.json")
OUTPUT_FOLDER = os.path.join(ABS_PATH, "") # Modificato per includere una sottocartella "output"

#data="1960 (63 yrs old)"
#match = re.search(pattern, data)
#print(match.group())

pattern = r'(?<!\d)\d{4}(?!\d)'
data = readJsonFile(INPUT_FOLDER)
for element in data:
    element["found_year"]=""
    anno = re.search(pattern, str(element["found_date"]))
    if anno:
        element["found_year"]=anno.group()

saveJsonFile(data,"outp.json")
