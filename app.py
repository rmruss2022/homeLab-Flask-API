from flask import Flask, jsonify
from flask_restful import Resource, Api
import RPi.GPIO as GPIO
import time
from flask_cors import CORS
import Adafruit_DHT
from flask import request
import datetime
import pytz

app = Flask(__name__)
api = Api(app)
CORS(app)

class home(Resource):
    def get(self):
        return "hello world"

class smartlock(Resource):
    def get(self):
        unlock()
        return jsonify({"get request" : "smart lock api"})

    def post(self):
        some_json = request.get_json()  
        exec('smartlocktest.py')
        return jsonify({"you sent: " : some_json})

class secFloorTemp_POST(Resource):
    def get(self):
        return getSecFloorTemp()
    def post(self):
        data = request.get_json()
        #print(data)
        current_time = datetime.datetime.now(pytz.timezone('America/New_York'))
        current_time = current_time.replace(tzinfo=None)
        file = open("log.txt", "a")
        file.write("sec floor temp posted: " + str(data["temperature"]) + "\n")
        file.close()
        f = open("tempPost.txt", "w")
        f.write(data["temperature"] + "\n")
        f.write(str(current_time))
        f.close()
        return data

class firstFloorTemp_POST(Resource):
    def get(self):
        return getFirstFloorTemp()
    def post(self):
        data = request.get_json()
        #print(data)
        current_time = datetime.datetime.now(pytz.timezone('America/New_York'))
        current_time = current_time.replace(tzinfo=None)
        file = open("log.txt", "a")
        file.write("first floor temp posted: " + str(data["temperature"]) + "\n")
        file.close()
        f = open("tempPost1.txt", "w")
        f.write(data["temperature"] + "\n")
        f.write(str(current_time))
        f.close()
        return data

class secFloorTemp_REAL_TIME(Resource):
    def get(self):
        #f = open("log.txt", "a")
        #f.write("current temp: " + str(getSecFloorTemp_RT()) + "\n")
        return getSecFloorTemp_RT()

api.add_resource(smartlock, '/smartlock')
api.add_resource(secFloorTemp_POST, '/secFloorTemp')
api.add_resource(firstFloorTemp_POST, '/firstFloorTemp')
api.add_resource(secFloorTemp_REAL_TIME, '/secFloorTempRT')
api.add_resource(home, '/')


def unlock():
    GPIO.setmode(GPIO.BCM)
    #GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) #button to gpio23
    GPIO.setup(24, GPIO.OUT) #led to gpio24
    GPIO.output(24, GPIO.HIGH)
    #print(GPIO.input(24))
    time.sleep(1)
    GPIO.output(24, GPIO.LOW)
    #print(GPIO.input(24))
    GPIO.cleanup()
    log = open("log.txt", "a")
    log.write("Door unlocked | TIME: " + str(datetime.datetime.now(pytz.timezone('America/New_York'))))
    log.write("---------------------------------------------------\n")
    log.close()

#if within 1 hr since a temperature
#was posted, return temp, otherwise -1
def getSecFloorTemp():
    f = open("tempPost.txt", "r")
    log = open("log.txt", "a")
    lines = f.readlines()
    log.write("getSecFloorTemp | TIME: " + str(datetime.datetime.now(pytz.timezone('America/New_York'))) + "\n")
    try:
        post_time = datetime.datetime.strptime(lines[1], '%Y-%m-%d %H:%M:%S.%f')
    except:
        log.write("Error in getting posted time, return -1\n")
        log.write("---------------------------------------------------\n")
        f.close()
        log.close()
        return -1
    f.close()
    
    current_time = datetime.datetime.now(pytz.timezone('America/New_York'))
    current_time = current_time.replace(tzinfo=None)
    time_difference_sec = (current_time - post_time).seconds
    #print(time_difference_sec)
    if (time_difference_sec > 3600):
        log.write("Time difference: " + str(time_difference_sec) + ", greater than hr, return -1\n")
        log.write("---------------------------------------------------\n")
        log.close()
        #print("time diff greater than 1 hr")
        return -1
    else:
        log.write("Posted time: " + str(time_difference_sec) + ", difference less than hr, return posted temp: " + str(lines[0]))
        log.write("---------------------------------------------------\n")
        log.close()
        #print("time diff less than 1 hr")
        #print(float(lines[0]))
        return float(lines[0])

#return real time value of temp sensor
def getSecFloorTemp_RT():
    log = open("log.txt", "a")
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = 4
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        temperature = temperature * 9 / 5 + 32
        log.write("Current temp called: " + str(temperature) + " | TIME: " + str(datetime.datetime.now(pytz.timezone('America/New_York'))) + "\n")
        log.write("---------------------------------------------------\n")
        log.close()
        return temperature
    else:
        log.write("Sensor failure. Check wiring | TIME: " + str(datetime.datetime.now(pytz.timezone('America/New_York'))) + "\n")
        log.write("---------------------------------------------------\n")
        log.close()
        return -1


#if within 1 hr since a temperature
#was posted, return temp, otherwise -1
def getFirstFloorTemp():
    f = open("tempPost1.txt", "r")
    log = open("log.txt", "a")
    lines = f.readlines()
    log.write("getFirstFloorTemp | TIME: " + str(datetime.datetime.now(pytz.timezone('America/New_York'))) + "\n")
    try:
        post_time = datetime.datetime.strptime(lines[1], '%Y-%m-%d %H:%M:%S.%f')
    except:
        log.write("Error in getting posted time, return -1\n")
        log.write("---------------------------------------------------\n")
        f.close()
        log.close()
        return -1
    f.close()
    
    current_time = datetime.datetime.now(pytz.timezone('America/New_York'))
    current_time = current_time.replace(tzinfo=None)
    time_difference_sec = (current_time - post_time).seconds
    #print(time_difference_sec)
    if (time_difference_sec > 3600):
        log.write("Time difference: " + str(time_difference_sec) + ", greater than hr, return -1\n")
        log.write("---------------------------------------------------\n")
        log.close()
        #print("time diff greater than 1 hr")
        return -1
    else:
        log.write("Posted time: " + str(time_difference_sec) + ", difference less than hr, return posted temp: " + str(lines[0]))
        log.write("---------------------------------------------------\n")
        log.close()
        #print("time diff less than 1 hr")
        #print(float(lines[0]))
        return float(lines[0])

if __name__ == '__maine__':
    app.run(debug=True) 
