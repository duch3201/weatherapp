import requests
import json
from geopy.geocoders import Nominatim
import sys
import os

geolocator = Nominatim(user_agent="MyApp")

os.chdir("configs")

if os.stat("usrloc.cfg").st_size == 0:

    usrloc = input(": ")
    with open("usrloc.cfg") as usr_loc_cfg:
        usr_loc_cfg.write(usrloc)
else:
    with open("usrloc.cfg") as usrloc_cfg:
        usrloc = usrloc_cfg.read()


location = geolocator.geocode(usrloc)

print("The latitude of the location is: ", location.latitude)
print("The longitude of the location is: ", location.longitude)



with open("apikey.cfg") as api_key_cfg:
    api_key = api_key_cfg.read()

#api_key = ""


lat = location.latitude
lon = location.longitude
url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
response = requests.get(url)
data = json.loads(response.text)
print("########|" + usrloc + "|########")
print("temperatura wynosi: " + str(data['current']['temp']) + "°C")
print("temperatura wynosi: " + str(data['current']['feels_like']) + "°C")
print("ciśninie wynosi: " + str(data['current']['pressure']))
print("wilgotność wynosi: "+ str(data['current']['humidity']))
print("chmury: "+ str(data['current']['clouds']))
print("widoczność: "+ str(data['current']['visibility']))
print("prędkość wiatru: "+ str(data['current']['wind_speed']))