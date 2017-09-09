# -*- coding: utf-8 -*-
#    
#   Created on: 06/09/2016
#   Author:     Nerigal
#   Version:    0.2.0
#   Purpose:    PRTG Custom Sensor Script


import sys
import json
from urllib.request import urlopen
import datetime
import time
import pytz

# as administrator
# . 'C:\Python34\python.exe' -m pip install pytz

from paepy.ChannelDefinition import CustomSensorResult

def is_dst(zonename):
 tz = pytz.timezone(zonename)
 now = pytz.utc.localize(datetime.datetime.utcnow())
return now.astimezone(tz).dst() != datetime.timedelta(0)

def BlockChainTimeStamp(pdata):
 params = json.loads(pdata['params'])
 url = "http://" + pdata['host'] + ":" + str(params['port']).rstrip() + "/api/blocks/?limit=1&offset=0&orderBy=height:desc"
 before = datetime.datetime.now()
 response = urlopen(url)
 data = json.loads(response.read().decode('utf8'))
 timestamp = data['blocks'][0]['timestamp']
 height = data['blocks'][0]['height']
 uptime = (datetime.datetime.now() - datetime.datetime(2016, 5, 24, 13, 00, 00)).total_seconds()
 timer = 0
 after = datetime.datetime.now()
 final = after - before
 if is_dst(str(params['tz'])) == True:  
  timer = ( (datetime.datetime.now() - datetime.datetime(2016, 5, 24, 13, 00, 00)).total_seconds() - timestamp )
 else:
  timer =  ( (datetime.datetime.now() - datetime.datetime(2016, 5, 24, 13, 00, 00)).total_seconds() - timestamp )
 if time.localtime().tm_isdst == 0: 
  timer = timer + 3600
 result = CustomSensorResult( 'Block Chain Status' )
 result.add_channel(channel_name="Block Age", unit="Custom", value=timer, is_float=False, is_limit_mode=True, primary_channel=True)
 result.add_channel(channel_name="Block Height", unit="Custom", value=height, is_float=False, is_limit_mode=True)
 return result.get_json_result() 

if __name__ == "__main__":
 data = json.loads(sys.argv[1])
 print(BlockChainTimeStamp(data))
