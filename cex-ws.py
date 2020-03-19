import asyncio
import websockets
import datetime
import time
import json
import hmac
import hashlib
import binascii
import base64

ts=str(int(datetime.datetime.now().timestamp()))
message = ts+'velQQ0qrGFQndtQUF2ZVEauufPQ'
secret = 's34IzqmLPGfgnXJPNjsHE8JEFg'
signature = hmac.new(bytes(secret , 'latin-1'), msg = bytes(message , 'latin-1'), digestmod = hashlib.sha256).hexdigest().upper()

pairs=[ 'BTC:USD',
        'ETH:USD',
        'XRP:USD',
        'LTC:USD',
        'BCH:USD',
        ]

pairs=['BTC:USD']

init={ 'e': 'init-ohlcv',
       'i': '1h',
       'rooms': [],
       }
auth= { 'e': 'auth',
        'auth': { 'key': 'velQQ0qrGFQndtQUF2ZVEauufPQ',
                  'timestamp': ts,
                  'signature': signature,
                },
        'oid': 'auth',
        }


auth_json=json.dumps(auth)

for p in pairs:
    init['rooms'].append('pair-{}'.format(p.replace(':','-')))
init_json=json.dumps(init)


#origin = "Origin: https://ws.cex.io"


async def cons(msg):
    print (msg)

async def process(uri):
    async with websockets.connect(uri) as websocket:
        message = await websocket.recv()
        print (message)
        await websocket.send(auth_json)
        message = await websocket.recv()
        print (message)
        await websocket.send(init_json)
        message = await websocket.recv()
        print (message)
        while True:
           message = await websocket.recv()
           #print (message)
           msg=json.loads(message)
           if msg['e'] == 'ping':
               await websocket.send('{"e":"pong"}')
           if msg['e'] == 'ohlcv1h':
               print (message)




print ('this is ticker')
uri='wss://ws.cex.io/ws'

loop = asyncio.get_event_loop()
loop.create_task(process(uri))
loop.run_forever()
