import os
import json
import country_converter as coco
import time
from geopy.geocoders import Nominatim
import translators as ts
from textblob import TextBlob

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(ABS_PATH, "json/parts/part_8.json")
OUTPUT_FOLDER = os.path.join(ABS_PATH, "json/fixed/")

def readJsonFile(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data

def saveJsonFile(data, output_file):
    with open(output_file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)

def cleanItalianAddress(element):
    raw_address = element["address"]
    componenti = raw_address.split(',')
    element["address"] = componenti[0].strip()
    element["location_city"] = componenti[1].strip()
    element["postal_code"] = componenti[2].strip()
    element["country"] = "Italy"

def fromCountryToCity(maybeCountry,geolocator):
    location = geolocator.geocode(maybeCountry)
    if location:
        return location.address.split(",")[-1].strip()
    else:
        return None

def convertCountry(country, country_labels, geolocator):
    # se country è nel dizionario me la restituisci subito
    if country in country_labels:
        return country_labels[country]
    
    # prova a tradurla subito
    #proc_country = ts.translate_text(country, translator="bing")
    # prova a convertirla
    label = coco.convert(country, to="name")
    if label != "not found":
        country_labels[country] = label
        return label
    else:
        # se la conversione non funziona, prova a convertire la city
        return convertCity(country, country_labels, geolocator)

def convertCity(city, country_labels, geolocator):
    if city in country_labels:
        print("cache hit city")
        return country_labels[city]
    
    country = fromCountryToCity(city, geolocator)
    if country:
        country_labels[city] = country
        return convertCountry(country, country_labels, geolocator)


""" def convertCountry(country, country_labels, geolocator):
    if country in country_labels:
        return country_labels[country]

    try:
        proc_country = ts.translate_text(country, translator="google")
    except Exception as e:
        print(f"Errore nella traduzione: {e}")
        proc_country = country  # Utilizza il nome originale in caso di errore

    label = coco.convert(names=proc_country, to='name_short')
    if label != "not found":
        country_labels[country] = label
        return label
    else:
        # Se non riesce a convertire direttamente il paese, prova con la città
        return convertCity(country, country_labels, geolocator)

def convertCity(city, country_labels, geolocator):
    if city in country_labels:
        print("cache hit city")
        return country_labels[city]

    country = fromCountryToCity(city, geolocator)
    if country:
        country_labels[city] = country
        return convertCountry(country, country_labels, geolocator)
    else:
        return "Country not found"
 """

def process_element(element, country_labels, geolocator):
    if ";" in str(element["found_date"]):
        element["found_date"] = str(element["found_date"]).split(';')[0]

    if "ITALY" in element["address"]:
        cleanItalianAddress(element)

    if element["country"]:
        element["country"] = convertCountry(element["country"],country_labels,geolocator)
        return element
    
    #proviamo a vedere se l'ultimo elemento dopo la virgola di location_city è una country
    elif element["location_city"]:
        #print("sono qui location city")
        forse_country = str(element["location_city"]).split(',')[-1].lstrip()
        country = convertCountry(forse_country,country_labels,geolocator)
        element["country"] = country
        
    elif (not element["country"]) and element["address"]:
            #print("sono qui address")
            forse_country = str(element["address"]).split(',')[-2].lstrip()
            country = convertCountry(forse_country,country_labels,geolocator)
            element["country"] = country
    
    #print(country_labels)
    return element

def main():
    data = readJsonFile(INPUT_FOLDER)
    new_data = []
    start_time = time.time()
    i = 0
    country_labels = {}
    geolocator = Nominatim(user_agent="wo")
    for element in data:
        if i%25 ==0:
            geolocator = Nominatim(user_agent=f"mini{i}")
        i += 1
        new_element = process_element(element, country_labels, geolocator)
        new_data.append(new_element)
        if i % 100 == 0:
            #print(country_labels)
            print(f"processati {i} elementi, trascorsi {time.time() - start_time} secondi")
        #if i % 500 == 0:
            #saveJsonFile(new_data, OUTPUT_FOLDER + f"_part_{i}.json")
    saveJsonFile(new_data, OUTPUT_FOLDER + "final_8.json")
    #print(country_labels)

if __name__ == "__main__":
    main()