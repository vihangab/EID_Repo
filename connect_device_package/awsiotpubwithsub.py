#!/usr/bin/python

# use this program to test the AWS IoT certificates received by the author
# to participate to the spectrogram sharing initiative on AWS cloud

# this program will publish test mqtt messages using the AWS IoT hub
# to test this program you have to run first its companion awsiotsub.py
# that will subscribe and show all the messages sent by this program

from __future__ import print_function # Python 2/3 compatibility
import sys
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


GPIO.setmode(GPIO.BOARD)

connflag = False
sensor =    22      #DHT22 sensor
pin =       4       #GPIO Pin 4 (Pin 7)
noisePin =  40      #GPIO Pin 21(Pin 40)
gasPin =    38;     #GPIO Pin 30(Pin 38)

GPIO.setup(noisePin, GPIO.IN)
GPIO.setup(gasPin, GPIO.IN)

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

#awshost = "aekn89lpwmp2q.iot.us-west-2.amazonaws.com"
#awsport = 8883
#clientId = "VB_Rpi3"
#thingName = "VB_Rpi3"
#caPath = "root-CA.crt"
#certPath = "VB_Rpi3.cert.pem"
#keyPath = "VB_Rpi3.private.key"

awshost = "a2vp65ivl2lw2v.iot.us-west-2.amazonaws.com"
awsport = 8883
clientId = "MyRPi3"
thingName = "MyRPi3"
caPath = "root-CA.crt"
certPath = "MyRPi3.cert.pem"
keyPath = "MyRPi3.private.key"


mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()

while 1==1:
    sleep(0.5)
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
    if connflag == True:
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
        result_json = {
  "Date":date_update,
  "Time":time_update,
  "Temperature":temperature,
  "Humidity": humidity,
  "Noise":noise_level,
  "Gas":gas_level
}
        mqttc.publish("temperature", json.dumps(result_json),0)
        #mqttc.publish("aws/things/VB_Rpi3/Temperature", tempreading, qos=1)
        print("msg sent: temperature " + str(temperature))
        print("msg sent: humidity " + str(humidity))
        print("msg sent: noise " + noise_level)
        print("msg sent: gas level " + gas_level)
        #response = table.query(
        #KeyConditionExpression=Key('topic').eq('temperature')) #FilterExpression=Attr('temperature').lt(30))
        #for i in response['Item']:
        #print(i['Date'], ":", i['Time'])
        #print(json.dumps(i, cls=DecimalEncoder))
        #items = response['Item']['Temperature']
        #items1 = response['Item']['Humidity']
        #items = response['Item']['Date']
        #print(i['Date'], ":", i['Time'])
        #print(json.dumps(i, cls=DecimalEncoder))    
    else:
        print("waiting for connection...")