import requests
import os
import time

API_URL = 'https://api.mist.com/api/v1'                         # API URL will change depending on your global 
TOKEN = os.getenv("INSERT YOUR TOKEN ENV")                      # Calling an environment variable
ORG_ID = '<INSERT YOUR ORG ID HERE>'                            # Add in the org ID

headers = { "Authorization": f"Token {TOKEN}"}

def getSites():
    # Block of code gets all sites in the specified Org
    url = f"{API_URL}/orgs/{ORG_ID}/sites"                      # The API url used to get all sites in the org
    r = requests.request("GET", url, headers=headers)           # Placing the result in the variable, r
    return r.json()                                             # Returning the result in json format

def getDevices(siteID):
    #Block of code gets all Connected access points in a site
    url = f"{API_URL}/sites/{siteID}/stats/devices"             # The API url used to get statistics on the network devices in a site
    r = requests.request("GET", url, headers=headers)           # Placing the result in the variable, r
    return r.json()                                             # Returning the result in json format
    
def main():
    sites = getSites()                                          # Placing the return from getSites() function into variable, sites
    totalAPsOnline = 0                                          # Initializing the variable with a zero integer

    timestamp = int(time.time() * 1000000000)                   # Getting timestamp in nanoseconds for InfluxDB

    for site in sites:                                          # Looping through each site
        # Block of code to get site ID
        siteID = site.get("id")                                 # Getting the Site ID and putting the result into the varialbe, siteID

        devices = getDevices(siteID)                            # Calling getDevices function and putting results into variable, devices
        for device in devices:
            # Block of code to get count all connected access points
            if device.get("type") != "ap":                      # Excluding all devices except an AP
                continue
            if device.get("status") == "connected":             # Only considering APs that are connected
                totalAPsOnline += 1
            
    #print(int(totalAPsOnline))
    print(f"mist_ap_summary,org_id={ORG_ID} total={totalAPsOnline} {timestamp}")
            
            

if __name__ == "__main__":
    main()
