from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import pickle
import datetime
import time

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

print("Accessing Rpi3 db")

#response = table.query(
#    KeyConditionExpression=Key('topic').eq('temperature')) #FilterExpression=Attr('temperature').lt(30))
date_update = datetime.datetime.now().strftime("%Y%m%d")
time_update = datetime.datetime.now().strftime("%H:%M")

response = table.get_item(Key={
'Date':date_update,
'Time':time_update
}
)
print(date_update)
print(time_update)

#for i in response['Item']:
#    print(i['Date'], ":", i['Time'])
    #print(json.dumps(i, cls=DecimalEncoder))


items = response['Item']['Temperature']
items1 = response['Item']['Humidity']
#items = response['Item']['Date']
#	print(i['Date'], ":", i['Time'])
#	print(json.dumps(i, cls=DecimalEncoder))

print(items)
print(items1)
