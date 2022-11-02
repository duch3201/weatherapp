from tempfile import tempdir
from flask import Flask, request, render_template, redirect, make_response, jsonify
from geopy.geocoders import Nominatim
from markupsafe import escape
import os
import requests
import json
import uuid
import time
from time import gmtime, strftime
import datetime
from datetime import datetime
import pytz

app = Flask(__name__)

# Load the OpenWeatherMap API key from ext file

apifile = open("apikey.k", 'r')
api_key = apifile.read()

def auth(apikey):
    print("auth")
    with open('apikeystxt') as myfile:
        print(apikey)
        print(myfile.read())
        if apikey in myfile.read():


            return True

def cache(action, returnd):
    if action == "create":
        with open('cache.txt', 'w') as f:
            f.write(str(returnd))
    elif action == "send":
        with open('cache.txt', 'r') as f:
            rtcache = f.read()
            return rtcache

def get_raw(city):
    geolocator = Nominatim(user_agent="weatherapp")
    api_key = "e23ccc0152024d943c58994cda4d2e27"
    location = geolocator.geocode(city)
    lat = location.latitude
    lon = location.longitude
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def get_weather(city, lang):
    
    #auth(apikey)

    #if CheckCache(timenow) == "cache expired":
     #   HasCacheExpired = True
    #else:
     #   HasCacheExpired = False
    
    if city == "null":
        city = "London"
    if lang == "null":
        lang = "en"

    geolocator = Nominatim(user_agent="weatherapp")
    #api_key = ""
    location = geolocator.geocode(city)
    lat = location.latitude
    lon = location.longitude
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
    response = requests.get(url)

    errorlist = ["305", "400", "401", "402", "403", "404", "405", "406", "407", "408", "409", "410", "411", "412", "413", "414", "415", "500", "503", "504"]

    if response.status_code in errorlist:
        return jsonify("received error code %s" % response.status_code)

    data = json.loads(response.text)

    if lang == "pl":

        #p = '{"responce": ["Python", "Java"]}'

        if "alerts" in data:
            alert = data['alerts'][0]['description']
            event = data['alerts'][0]['event']
        else:
            alert = "none"
            event = "none"

        #alert = "temperatura wynosi: " + str(data['alerts']['description'])
        #print(alert)
        #asender = "temperatur3a wynosi: " + str(data['alerts'][1])
        #print(asender)
        #alert = data['alert'][0]['description']
        #img = data['current']['weather'][0]['description']
        otemp = data['current']['temp']
        oftemp = data['current']['feels_like']
        
        sunset_time = data['current']['sunset']

        temp = str(round(otemp, 1)) + "°"
        status = data['current']['weather'][0]["description"]
        ftemp = "odczuwalna temperatura " + str(round(oftemp, 1)) + "°"
        pres = "ciśninie wynosi: " + str(data['current']['pressure']) + "hPa"
        humidity = "wilgotność wynosi: "+ str(data['current']['humidity']) + "%"
        clouds = "chmury: "+ str(data['current']['clouds'])
        visibility = "widoczność: "+ str(data['current']['visibility'])
        wind_speed = "prędkość wiatru: "+ str(data['current']['wind_speed']) + "m/s"
        #return_data = '{ "alert":alert "temp":temp, "ftemp":ftemp, "pres":pres, "humidity":humidity, "clouds":clouds, "visibility":visibility, "wind_speed":wind_speed}'
        return_data = temp + "\n" + ftemp + "\n" + pres + "\n" + humidity + "\n" + clouds + "\n" + visibility + "\n" + wind_speed
        #print(return_data)

        timezone = pytz.timezone(data['timezone'])
        timeold = datetime.now(timezone)
        time = timeold.strftime("%H:%M")

        returnd={
        "responce": {
            "alert": alert,
            "event": event,
            #"img": img,
            #"asender": asender,
            "time": time,
            "temp": temp,
            "ftemp": ftemp,
            "status": status,
            "wind_speed": wind_speed
        }
        }
        #rint(jsonify(return_data))

        #if HasCacheExpired == False:
         #   return_cachedata(returnd)
          #  print("cache updated")
           # return return_cachedata() 
        #else:
        return jsonify(returnd)

        
    elif lang == "en":

        if "alerts" in data:
            alert = data['alerts'][0]['description']
            event = data['alerts'][0]['event']
        else:
            alert = "none"
            event = "none"

        status = data['current']['weather'][0]['description']
        otemp = data['current']['temp']
        oftemp = data['current']['feels_like']
        
        temp = str(round(otemp, 1)) + "°"
        ftemp = "Feels Like " + str(round(oftemp, 1)) + "°"
        pres = "pressure: " + str(data['current']['pressure']) + "hPa"
        humidity = "humidity: "+ str(data['current']['humidity']) + "%"
        clouds = "clouds: "+ str(data['current']['clouds'])
        visibility = "visibility: "+ str(data['current']['visibility'])
        wind_speed = "wind speed "+ str(data['current']['wind_speed']) + "m/s"
        return_data = temp + "\n" + ftemp + "\n" + pres + "\n" + humidity + "\n" + clouds + "\n" + visibility + "\n" + wind_speed
        #print(return_data)    

        timezone = pytz.timezone(data['timezone'])
        timeold = datetime.now(timezone)
        time = timeold.strftime("%H:%M")

        returnd={
        "responce": {
            "alert": alert,
	    "status": status,
            "event": event,          
            "time": time,            
            "temp": temp,
            "ftemp": ftemp,
            "wind_speed": wind_speed
        }
        }

        return returnd

        #if HasCacheExpired == True:
         #   cachedata(returnd)
          #  print("cache updated")
        #else:
         #   return returnd

@app.route("/get-weather/<city>/<lang>")
def main(city, lang):
    #get_weather(city)
    return get_weather(city, lang)
    #return jsonify("504")

@app.route("/rawdata/<city>/")
def raw(city):
    return get_raw(city)

@app.route("/test")
def test():
    return render_template("index copy.html")

@app.route("/devtest")
def devtest():
    return render_template("devtest.html")



@app.route('/response', methods=['POST'])
def response():
    city = request.form.get("city")
    res = make_response("/get-city-cookie") 
    res.set_cookie('city', city)
    return res

@app.route("/testui")
def testui():
    #data = get_weather("bydgoszcz", "en")
    return render_template('index.html')

@app.route("/isOnline")
def isOnline():

    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric"
    r = requests.head(url)
    if r.status_code == 401:
        openweatherapi = "online"
    else:
        openweatherapi = "offline"

    returnd={
        "responce": {
            "openweatherapi": openweatherapi
        }
        }
    return returnd

@app.route("/?source=pwa")
def pwa():
    return render_template("devtest.html")

@app.route("/")
def root():
    return render_template("devtest.html")

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000, debug=True)
