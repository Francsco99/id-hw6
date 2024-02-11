import json
import os

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(ABS_PATH, "json/final_table.json")
OUTPUT_FOLDER = os.path.join(ABS_PATH, "json/fixed/")

def readJsonFile(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data

def saveJsonFile(data, output_file):
    with open(output_file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)

data = readJsonFile(INPUT_FOLDER)
no_addres=0
no_city=0
no_country=0

no_addres_country=0
no_addres_city=0
no_city_country=0
no_addres_country_city=0

num_elementi=0

no_found_date=0
for element in data:
    if (not element["location_city"])and(not element["country"]and (not element["address"])):
        no_addres_country_city+=1
    if (not element["location_city"])and(not element["country"]):
        no_city_country+=1
    if (not element["address"])and(not element["country"]):
        no_addres_country+=1
    if (not element["location_city"])and(not element["address"]):
        no_addres_city+=1
    if (not element["location_city"]):
        no_city+=1
    if not element["country"]:
        no_country+=1
    if(not element["address"]):
        no_addres+=1
    if(not element["found_date"]):
        no_found_date+=1
    num_elementi+=1

print("No address: ",no_addres)
print("No city: ",no_city)
print("No country: ",no_country)
print("No address-city: ",no_addres_city)
print("No address-country: ",no_addres_country)
print("No country-city: ",no_city_country)
print("No address-contry-city: ",no_addres_country_city)
print("No found-date: ",no_found_date)
print("Numero di elementi: ",num_elementi)