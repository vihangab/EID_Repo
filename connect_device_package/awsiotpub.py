#!/usr/bin/env python3

#############################################################
# Authors: Vihanga Bare and Virag Gada
# File name : awsiotpub.py
# Description : main file to run on sensor hub which collects
# data from the sensors and also Vehicle count using OpenCV
# to AWS IoT using MQTT
# Use: Use this program with AWS IoT certificates and Thing 
# keys to send data to AWS IoT. Run using Python3.5 to support
# aiocoap library.
# Program runs in a continuous while loop and published data
# to AWS IOT thing. We can stop publishing once this program
# receives such a command from client RPI3 through COAP and
# dynamoDB
############################################################

#import required modules
from __future__ import print_function # Python 2/3 compatibility
import sys
sys.path.append('/usr/local/lib/python3.5/site-packages')
import numpy.core.multiarray
import cv2
import time
import Adafruit_DHT
import paho.mqtt.client as paho
import os
import socket
import ssl
import json
import datetime
from time import sleep
from random import uniform
import RPi.GPIO as GPIO
import boto3
import json
import decimal
import pickle


#Set GPIO mode to Board pins
GPIO.setmode(GPIO.BOARD)

#Set Global variables
connflag = True
sensor =    22      #DHT22 sensor
pin =       4       #GPIO Pin 4 (Pin 7)
noisePin =  40      #GPIO Pin 21(Pin 40)
gasPin =    38      #GPIO Pin 30(Pin 38)
Count =     0

#Set GPIO pins as input
GPIO.setup(noisePin, GPIO.IN)
GPIO.setup(gasPin, GPIO.IN)

#humidity = 42.2 #hardcoded values only for debugging
#temperature = 24.2 #hardcoded values only for debugging

from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

class PythonObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return super(PythonObjectEncoder, self).default(self)#{'_python_object': pickle.dumps(obj)}

class SetEncoder(json.JSONEncoder):
     def default(self, obj):
          if isinstance(obj, set):
             return list(obj)
          return json.JSONEncoder.default(self, obj)

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')#, endpoint_url="https://dynamodb.us-west-2.amazonaws.com/")

table = dynamodb.Table('RPI3_Data')
table1 = dynamodb.Table('RPI_Data')

print("Accessing Rpi3 db")

#Capture video from the given file
cap = cv2.VideoCapture('video.avi')

# Trained XML classifiers describes some features of some object we want to detect
car_cascade = cv2.CascadeClassifier('cars.xml')

# Define handlers for MQTT events
def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log

#Keys and certificate for Vihanga's IoT
#awshost = "aekn89lpwmp2q.iot.us-west-2.amazonaws.com"
#awsport = 8883
#clientId = "VB_Rpi3"
#thingName = "VB_Rpi3"
#caPath = "root-CA.crt"
#certPath = "VB_Rpi3.cert.pem"
#keyPath = "VB_Rpi3.private.key"

#Keys and certificate for Virag's AWS IoT
awshost = "a2vp65ivl2lw2v.iot.us-west-2.amazonaws.com"
awsport = 8883
clientId = "MyRPi3"
thingName = "MyRPi3"
caPath = "root-CA.crt"
certPath = "MyRPi3.cert.pem"
keyPath = "MyRPi3.private.key"

#Set the keys and certificates for MQTT thing
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()

while 1==1:
    sleep(10)
    response = table1.get_item(Key={
        'UserID':1001,
        'Username':"Vihanga"
}
)
    item = response['Item']['System']
    if (str(item) =="b'ON'"):
        print(str(item))
        connflag = True
    else:
        connflag = False

    #Start when connected to a topic
    if connflag == True:
        # reads frames from a video
        ret,frames=cap.read()
        # convert to gray scale of each frames
        gray = cv2.cvtColor(frames,cv2.COLOR_BGR2GRAY)

        # Detects cars of different sizes in the input image
        cars = car_cascade.detectMultiScale(gray, 1.1, 1)

        # To draw a rectangle in each cars
        for (x,y,w,h) in cars:
                cv2.rectangle(frames,(x,y),(x+w,y+h),(0,0,255),2)
        
        #Read Sensor values
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        temperature = round(temperature,2)
        humidity = round(humidity,2)
        noise = GPIO.input(noisePin)
        gas = GPIO.input(gasPin)
        sleep(1)
        if noise:
            noise_level = "Loud"
        else:
            noise_level = "Quiet"
        if gas:
            gas_level = "Polluted"
        else:
            gas_level = "Clean"
        date_update = datetime.datetime.now().strftime("%Y%m%d")
        time_update= datetime.datetime.now().strftime("%H:%M")
        
        #Add to JSON packet
        result_json = {
  "Date":date_update,
  "Time":time_update,
  "Temperature":temperature,
  "Humidity": humidity,
  "Noise":noise_level,
  "Gas":gas_level,
  "Vehicle Count":len(cars)
}
        mqttc.publish("temperature", json.dumps(result_json),0)
        #mqttc.publish("aws/things/VB_Rpi3/Temperature", tempreading, qos=1)
        print("msg sent: temperature " + str(temperature))
        print("msg sent: humidity " + str(humidity))
        print("msg sent: noise " + noise_level)
        print("msg sent: gas level " + gas_level)
        print("msg sent: Vehicle count= "+str(len(cars)))
    else:
        print("waiting for connection...")
