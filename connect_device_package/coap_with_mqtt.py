#!/usr/bin/env Python
from __future__ import print_function # Python 2/3 compatibility
import sys
import time
import datetime
import json
import decimal
import pickle
import sys
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap

import Adafruit_DHT
import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
from random import uniform
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

connflag = False
sensor =    22      #DHT22 sensor
pin =       4       #GPIO Pin 4 (Pin 7)
noisePin =  40      #GPIO Pin 21(Pin 40)
gasPin =    38;     #GPIO Pin 30(Pin 38)

GPIO.setup(noisePin, GPIO.IN)
GPIO.setup(gasPin, GPIO.IN)

class BlockResource(resource.Resource):
    """
    Example resource which supports GET and PUT methods. It sends large
    responses, which trigger blockwise transfer.
    """

    def __init__(self):
        super(BlockResource, self).__init__()
        self.content = ("This is the resource's default content. It is padded "\
        "with numbers to be large enough to trigger blockwise "\
        "transfer.\n" + "0123456789\n" * 100).encode("ascii")

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.content = request.payload
        payload = ("I've accepted the new payload. You may inspect it here in "\
                "Python's repr format:\n\n%r"%self.content).encode('utf8')
        return aiocoap.Message(payload=payload)


class SeparateLargeResource(resource.Resource):
    """
    Example resource which supports GET method. It uses asyncio.sleep to
    simulate a long-running operation, and thus forces the protocol to send
    empty ACK first.
    """

    def __init__(self):
        super(SeparateLargeResource, self).__init__()
#        self.add_param(resource.LinkParam("title", "Large resource."))
#        self.add_param(resource.LinkParam("title", "Large resource."))

    async def render_get(self, request):
        await asyncio.sleep(3)

        payload = "Three rings for the elven kings under the sky, seven rings"\
                "for dwarven lords in their halls of stone, nine rings for"\
                "mortal men doomed to die, one ring for the dark lord on his"\
                "dark throne.".encode('ascii')
        return aiocoap.Message(payload=payload)

class TimeResource(resource.ObservableResource):
    """
    Example resource that can be observed. The `notify` method keeps scheduling
    itself, and calles `update_state` to trigger sending notifications.
    """
    def __init__(self):
        super(TimeResource, self).__init__()

        self.notify()

    def notify(self):
        self.updated_state()
        asyncio.get_event_loop().call_later(6, self.notify)

    def update_observation_count(self, count):
        if count:
            # not that it's actually implemented like that here -- unconditional updating works just as well
            print("Keeping the clock nearby to trigger observations")
        else:
            print("Stowing away the clock until someone asks again")

    async def render_get(self, request):
        datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json_time = json.dumps(datenow)
        print(json_time)
        print('Timestamp:',json_time)
        self.content = ("Timestamp :"+json_time).encode("ascii")
        return aiocoap.Message(payload=self.content)
    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.content = request.payload
        payload = ("Received payload as :\n\n%r"%self.content).encode('utf8')
        return aiocoap.Message(payload=payload)
# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))

    root.add_resource(('time',), TimeResource())

    root.add_resource(('other', 'block'), BlockResource())

    root.add_resource(('other', 'separate'), SeparateLargeResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    
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
    count = 0

    while (count<20):
        sleep(0.5)

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
        else:
            print("waiting for connection...")

    count = count +1
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
