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
    url_path = '/api/delegates/get/?publicKey=' + params['publicKey']
    url_voters = '/api/delegates/voters?publicKey=' + params['publicKey']
    found_url_path = '/api/accounts/getBalance?address=' + params['address']

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
        found_url = protocol + '://' + servername + port + found_url_path
        voter_url = protocol + '://' + servername + port + url_voters
        try:
            response = urlopen(url)           
            found_response = urlopen(found_url)
            voter_response = urlopen(voter_url)
            
            data = json.loads(response.read().decode('utf8'))
            found_data = json.loads(found_response.read().decode('utf8'))
            voter_data = json.loads(voter_response.read().decode('utf8'))

            if data['success'] == True and found_data['success'] == True:
                ret = True
                break
        except:
            pass

    if ret == True:
        vvalue = 0
        for vv in voter_data['accounts']:
            vvalue = vvalue + int(vv['balance'])    
        result = CustomSensorResult("Forging Productivity")
        # add primary channel
        result.add_channel(channel_name="Forging Productivity", unit="Custom", value=data['delegate']['productivity'], is_float=True, is_limit_mode=True, primary_channel=True)
        result.add_channel(channel_name="Forging ProducedBlocks", unit="Custom", value=data['delegate']['producedblocks'], is_float=False, is_limit_mode=True, primary_channel=False)
        result.add_channel(channel_name="Forging MissedBlocks", unit="Custom", value=data['delegate']['missedblocks'], is_float=False, is_limit_mode=True, primary_channel=False)
        result.add_channel(channel_name="Forging Approval", unit="Custom", value=data['delegate']['approval'], is_float=True, is_limit_mode=True, primary_channel=False)
        result.add_channel(channel_name="Forging Found", unit="Custom", value=int(found_data['balance'])/100000000, is_float=True, is_limit_mode=True, primary_channel=False)
        result.add_channel(channel_name="Forging Rate", unit="Custom", value=data['delegate']['rate'], is_float=False, is_limit_mode=False, primary_channel=False)
        result.add_channel(channel_name="Voters Count", unit="Custom", value=len(voter_data['accounts']), is_float=False, is_limit_mode=False, primary_channel=False)
        result.add_channel(channel_name="Voters Found", unit="Custom", value=vvalue/100000000, is_float=True, is_limit_mode=True, primary_channel=False)
print(result.get_json_result()) 