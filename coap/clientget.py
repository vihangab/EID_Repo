#!/usr/bin/env python
import logging
import asyncio
import json

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://54.71.205.59/time')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))
        items = response.payload.decode('utf-8')
        items = str(items)
        #mylist = items.replace('{',' ').replace('\'',' ').replace(':',' ').replace(',',' ').split()
        #print(mylist) 
        print(items) 

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
