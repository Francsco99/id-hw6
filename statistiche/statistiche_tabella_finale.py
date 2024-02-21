import json
import os


INPUT_FOLDER = '/Users/fspezzano/vscode/id-hw6/hw3_integration/json/paired.json'


def readJsonFile(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data

def saveJsonFile(data, output_file):
    with open(output_file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)

data = readJsonFile(INPUT_FOLDER)
'''
risultato ={}
for element in data:
    for attributo in element:
        if element[attributo]=="":
            if attributo in risultato:
                risultato[attributo]+=1
            else:
                risultato[attributo]=1
somma=0
for k,v in sorted(risultato.items()):
    print(f'Attributo: {k}: {v} elementi nulli')
    somma+=v
print(f"{somma} elementi nulli in totale")
'''

no_addres=0
no_city=0
no_country=0

no_addres_country=0
no_addres_city=0
no_city_country=0
no_addres_country_city=0
no_industry=0
no_sector=0
num_elementi=0
no_name=0
nulli=0
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
    if(not element["sector"]):
        no_sector +=1
    if(not element["industry"]):
        no_industry +=1
    if(not element["company_name"]):
        no_name+=1
    num_elementi+=1
    for k,v in element.items():
        if v=='':
            nulli+=1
print("No address: ",no_addres)
print("No city: ",no_city)
print("No country: ",no_country)
print("No address-city: ",no_addres_city)
print("No address-country: ",no_addres_country)
print("No country-city: ",no_city_country)
print("No address-contry-city: ",no_addres_country_city)
print("No found-date: ",no_found_date)
print("No industry: ",no_industry)
print("No sector: ",no_sector)
print("No name: ",no_name)
print("Numero di elementi: ",num_elementi)
print("Elementi nulli: ",nulli)