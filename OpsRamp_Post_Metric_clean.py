#!/usr/bin/python
# =====================================================================================================
# Author  : Eric Repec (eric.repec@mysticriver.consulting)
# Version: 0.4
# Date created: 5/1/2020
# Description: Python example to post metric to OpsRamp Metric API V2
# =====================================================================================================

import time
import json
import requests

# Define the Metric Payload
# URL: https://docs.pov.opsramp.com/metric-apis/#Save_Metrics_on_a_Resource
metric_json = [{
        "metricName": "EnergyUsage",
        "instanceVal": "0",
        "ts": time.mktime(time.localtime())
    }]

# Tenant credentials
# client = {
#     'suffix':'mysticriver',
#     'tenant_id':'client_88',
#     'rtype':'Linux',
#     'resource_guid':'<resource GUID>',
#     'key':'<OAuth Key>',
#     'secret':'<OAuth Secret>'
# }

with open('OpsRampTenantCredentials.json','r') as f:
    client = json.load(f)
    
# Build Base URIs
base_uri = 'https://'+client['suffix']+'.api.pov.opsramp.com'
base_api_uri = base_uri+'/api/v2/metric/tenants/'+client['tenant_id']

def build_access_header():
    # Post OAuth2 token and build access_header for submission
    headers = {"Content-Type": "application/x-www-form-urlencoded","Accept": "application/json"}
    
    # Key and Secret are generated in the OpsRamp GUI under Setup~Integrations~Other~"Custom Integration" 
    data = {"grant_type": "client_credentials","client_id": client['key'],"client_secret": client['secret']}
    
    auth_uri = base_uri+'/auth/oauth/token'
    r = requests.post(auth_uri,data=data,headers=headers)
    print('\nAuthentication Post Status Code: '+str(r.status_code))
    if r.status_code != 200:
        print('\nAuthentication Post Response: ' + str(r.content))
    json = r.json()
    auth = str(json["token_type"]) + " " + str(json["access_token"])
    global access_header
    access_header = {"Content-Type": "application/json", "Accept": "application/json","Authorization": auth}
    print ("Captured Access Header %s " % access_header)

def post_metric():
    # Create metric
    create_metric_uri = base_api_uri+'/rtypes/'+client['rtype']+'/resources/'+client['resource_guid']+'/metrics'
    # Unpack JSON object into string
    json_out = json.dumps(metric_json,indent=4) 
    print("\nMetic Payload: \n"+json_out)
    r = requests.post(create_metric_uri,headers=access_header,data=json_out)
    print('\nMetric Post Status Code: '+str(r.status_code))
    if r.status_code != 200:
        print('\nFailed Metric Post Response: ' + str(r.content))


# Dummy data generation stub
values = ["300","400","500","500","500","1200","1200","1200","1200","1200","1500","1500","2000","2000","3000","4000","5000","5000","5000","2000","300","400","500","500","500","1200","1200","1200","1200","1200","1500","1500","2000","2000","3000","4000","5000","5000","5000","2000"]
for i in values:
    print (i)
    for a in range(12):
        build_access_header()
        for item in metric_json:
            item['instanceVal']=i
            item['ts']=time.mktime(time.localtime())
        post_metric()
        time.sleep(60)
