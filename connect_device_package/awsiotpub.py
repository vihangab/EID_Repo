#!/usr/bin/python

# this source is part of my Hackster.io project:  https://www.hackster.io/mariocannistra/radio-astronomy-with-rtl-sdr-raspberrypi-and-amazon-aws-iot-45b617

# use this program to test the AWS IoT certificates received by the author
# to participate to the spectrogram sharing initiative on AWS cloud

# this program will publish test mqtt messages using the AWS IoT hub
# to test this program you have to run first its companion awsiotsub.py
# that will subscribe and show all the messages sent by this program

import paho.mqtt.client as paho
import os
import socket
import ssl
import json
import datetime
from time import sleep
from random import uniform

connflag = False

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
    if connflag == True:
        tempreading = uniform(15.0,25.0)
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
        result_json={'UserID':1005,'Username':"Virag", 'Temp':tempreading}
        mqttc.publish("temperature",json.dumps(result_json),0)
        #mqttc.publish("aws/things/VB_Rpi3/Temperature", tempreading, qos=1)
        print("msg sent: temperature " + "%.2f" % tempreading )
    else:
        print("waiting for connection...")
