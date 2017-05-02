#!/usr/bin/env python
#importing required libraries
from __future__ import print_function # Python 2/3 compatibility
from boto3.dynamodb.conditions import Key, Attr
import sys
import time
import datetime
#import Adafruit_DHT
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import datetime
import time
import json
from tornado import web
#from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import pickle
#from boto3.dynamodb.conditions import Key, Attr
#sensor = 22
#pin = 4
#temperature
#humidity
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

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("/var/www/index.html")
        datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json_data = json.dumps(datenow)
        print(json_data)

class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self):
        print ('New connection was opened')
        self.write_message("Welcome to my websocket!")
    def on_message(self, message):
        print ('Incoming message:', message)
        self.write_message("Request : " + message)
        if message =="temp":
            dynamodb = boto3.resource('dynamodb', region_name='us-west-2')#, endpoint_url="https://dynamodb.us-west-2.amazonaws.com/")
            table = dynamodb.Table('RPI_Data')
            print("Accessing Rpi3 db")
            #humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            #temperature = 23#round(temperature,2)
            #humidity = 25#round(humidity,2)
            #response = table.query(
            #KeyConditionExpression=Key('topic').eq('temperature')) #FilterExpression=Attr('temperature').lt(30))
            #dynamodb = boto3.resource('dynamodb', region_name='us-west-2')#, endpoint_url="https://dynamodb.us-west-2.amazonaws.com/")
            #table = dynamodb.Table('RPI_Data')
            response=table.get_item(Key={'UserID':1005,'Username':'Virag'})
            #for i in response['Item']:
            #print(i['topic'], ":", i['timestamp'])
            #print(json.dumps(i, cls=DecimalEncoder))
            items = response['Item']['Temp']
            print(items)
            datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #json_data = json.dumps(items)
            json_time = json.dumps(datenow)
            #print(json_data)
            print(json_time)
            print('Incoming request:', message)
            print('Incoming request:', message)
            print('Timestamp:',json_time)
            print('Temperature:',items)
            self.write_message("Request: " + message)
            self.write_message("Temperature :"+str(items))
            self.write_message("Timestamp :"+ json_time)
        if message =="humidity":
            #humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            #temperature = #round(temperature,2)
            humidity = 25#round(humidity,2)
            datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            json_data = json.dumps(str(humidity))
            json_time = json.dumps(datenow)
            json_data1 = json.dumps(str(temperature))
            print(json_data)
            print(json_time)
            print(json_data1)
            print('Incoming request:', message)
            print('Timestamp:',json_time)
            print('Humidity:',json_data)
            self.write_message("Request: " + message)
            self.write_message("Response :"+json_data)
            self.write_message("Timestamp :"+json_time)
            self.write_message("Temperature :"+json_data1)

    def on_close(self):
        print ('Connection was closed...')
application = tornado.web.Application([
   (r'/ws', WSHandler),(r'/', IndexHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

