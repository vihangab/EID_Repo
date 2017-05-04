from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import pickle
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

table = dynamodb.Table('RPI_Data')

print("Accessing Rpi3 db")

response = table.put_item(
   Item={
        'UserID': 1003,
        'Username': "Virag",
        'Temp': '33'
 }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))

