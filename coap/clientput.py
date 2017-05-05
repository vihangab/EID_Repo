#!/usr/bin/env python
import logging
import asyncio

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    """
    Example class which performs single PUT request to localhost
    port 5683 (official IANA assigned CoAP port), URI "/other/block".
    Request is sent 2 seconds after initialization.
    Payload is bigger than 1kB, and thus is sent as several blocks.
    """

    context = await Context.create_client_context()

    await asyncio.sleep(2)

    payload = b"Temperature update received"
    request = Message(code=PUT, payload=payload)
    request.opt.uri_host = '54.71.205.59'
    request.opt.uri_path = ("time",)

    response = await context.request(request).response

    print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
