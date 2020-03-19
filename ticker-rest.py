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
logfile=f'{symbol1}-{symbol2}.log'
url=f'https://cex.io/api/trade_history/{symbol1}/{symbol2}/'

'''
if len(sys.argv) > 3:
    proxies={ 'http': 'http://10.48.202.79:8888'
              'https': 'http://10.48.202.79:8888'
            }
else:
'''
proxies={}

ptr=0
t={}

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'trade_history_cex')
client.create_database('trade_history_cex')

while True:
    try:
        t=json.loads(r.get(url, proxies=proxies).text)
    except:
        pass
    cnt, c_date = 0,0
    for tt in t[::-1]:
        c_type, c_date, c_amount, c_price, _ = tt.values()
        if int(c_date) > ptr:
            cnt+=1
            db_point = ([
                {
                    "measurement": f"CEX-{symbol1}-{symbol2}",
                    "time": f"{(datetime.datetime.fromtimestamp(int(c_date))  - datetime.timedelta(hours=3)).isoformat()}",
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
        print (f'{datetime.datetime.now()} {symbol1}:{symbol2} {cnt} new records')
        log=open(logfile,'a')
        log.write (f'{datetime.datetime.now()} {symbol1}:{symbol2} {cnt} new records\n')
        log.close()
    time.sleep(loop_sec+random.randint(0,10))


