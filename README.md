# Lisk Python Monitoring script for PRTG 
Python Monitoring script for PRTG

**PRTG-ForgingState.py** Will give you information about your delegate state


**PRTG-ForgingStatus.py** Will return the forging status of your delete, so you can configure alert if your delegate has stop forging


**PRTG-BlockChainTimeStamp.py** Will give you the time stamp of the server you are querying, You can then trigger alerts if the block age is higher than 30 sec for a warning, 60 second for an Alert, as per block should last 10 sec...


**PRTG-ForgingState** and **PRTG-ForgingStatus** :

JSON arg Example to pass to you code using sensor "Additional Parameters" :
you will need to edit and fit to your setup

`{  "servers" : [ { "hostname": "<SERVER_NAME>", "ip": "1.2.3.4", "port" : "" }, { "hostname": "<SERVER_NAME>", "ip": "5.6.7.8", "port" : "" }],   "publicKey" : "<MY_PUBLICKEY>",  "address" : "<MY_DELEGATE_ADDRESS>",  "force_ssl" : "True" }` 

**PRTG-BlockChainTimeStamp** :

`{ "port" : "8000" , "tz" : "America/New_York" }`
