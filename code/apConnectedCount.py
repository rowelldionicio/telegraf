import requests
import os
import time

API_URL = 'https://api.mist.com/api/v1'                                     # API URL will change depending on your global location
TOKEN = os.getenv("<INSERT YOUR TOKEN ENV>")                                # Calling an environment variable
ORG_ID = '<INSERT YOUR ORG ID HERE>'                             			# Add in your org ID

headers = { "Authorization": f"Token {TOKEN}"}

def getDevices():
    #Block of code gets all Connected access points in the org
    url = f"{API_URL}/orgs/{ORG_ID}/devices/count?distinct=model&type=ap"   # Getting list of APs
    r = requests.request("GET", url, headers=headers)                       # Placing the result in the variable, r
    return r.json()                                                         # Returning the result in json format
    
def main():
    devices = getDevices()                                                  # Adding APs to the devices variable
    totalAPsOnline = 0                                                      # Initializing the variable with a zero integer

    timestamp = int(time.time() * 1000000000)                               # Getting timestamp in nanoseconds for InfluxDB
    
    for device in devices.get("results", []):                               # Looping through each device and counting
        totalAPsOnline += device.get("count", 0)   
        
    print(f"mist_ap_summary,org_id={ORG_ID} total={totalAPsOnline} {timestamp}")        
            

if __name__ == "__main__":
    main()
