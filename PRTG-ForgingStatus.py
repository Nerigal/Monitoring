# -*- coding: utf-8 -*-
#    
#   Created on: 12/09/2016
#   Author:     Nerigal
#   Version:    0.2.0
#   Purpose:    PRTG Custom Sensor Script

import sys
import json
from urllib.request import urlopen
from paepy.ChannelDefinition import CustomSensorResult

if __name__ == "__main__":
    pdata = json.loads(sys.argv[1])
    params = json.loads(str(pdata['params']))   
    url_path = '/api/delegates/forging/status?publicKey=' + params['publicKey']

    ret = False
    for server in params['servers']:
        port = ''
        if server['port'] != '':
            port = ':' + server['port']

        if params['force_ssl'] != 'True':
            servername = server['ip']
            protocol = 'http'
        else:
            servername = server['hostname']
            protocol = 'https'
            
        url = protocol + '://' + servername + port + url_path    
        try:
            response = urlopen(url)
            data = json.loads(response.read().decode('utf8'))
            if data['success'] == True and data['enabled'] == True :
                ret = True
                break
        except:
            pass
    # create sensor result
    if ret == True :
        result = CustomSensorResult("Forging Status Active")
        # add primary channel
        result.add_channel(channel_name="Forging Status", unit="Custom", value=1, is_float=False, is_limit_mode=True, primary_channel=True)
    else:
        result = CustomSensorResult("Forging Disable")
        result.add_channel(channel_name="Forging Status", unit="Custom", value=0, is_float=False, is_limit_mode=True, primary_channel=True)
        result.add_error("Forging Disable")
    print(result.get_json_result())
