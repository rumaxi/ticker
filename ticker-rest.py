import requests as r 
import datetime
import random
import json
import time
import sys
from influxdb import InfluxDBClient


loop_sec=10
symbol1=sys.argv[1]
symbol2=sys.argv[2]
url=f'https://cex.io/api/trade_history/{symbol1}/{symbol2}/'

ptr=0

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'trade_history_cex')
client.create_database('trade_history_cex')

while True:
    t=json.loads(r.get(url).text)
    cnt, c_date = 0,0
    for tt in t[::-1]:
        c_type, c_date, c_amount, c_price, _ = tt.values()
        if int(c_date) > ptr:
            cnt+=1
            db_point = ([
                {
                    "measurement": f"CEX-{symbol1}-{symbol2}",
                    "time": f"{datetime.datetime.fromtimestamp(int(c_date)).isoformat()}",
                    "fields": {
                        "type": c_type,
                        "date": c_date,
                        "amount": c_amount,
                        "price": c_price,
                    }
                }
            ])
            client.write_points(db_point)


    ptr=int(c_date)
    if cnt:
        print (f'{datetime.datetime.now()} {symbol1}:{symbol2} {cnt} new records ptr:{ptr}')
    time.sleep(loop_sec+random.randint(0,10))


