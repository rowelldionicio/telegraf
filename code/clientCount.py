import requests
import os
import time

"""
Written by Rowell Dionicio (@rowelldionicio)
Created on: November 15, 2025
This script iterates through all sites in an organization to gather total client count and outputs for Telegraf
The token is stored in an environmental variable.
"""

API_URL = 'https://api.mist.com/api/v1'                         # API URL will change depending on your global 
TOKEN = os.getenv("<ENTER-YOUR-TOKEN-ENV-VARIABLE>")            # Calling an environment variable
ORG_ID = '<ENTER-YOUR-ORG-ID>'                                   # Add in the org ID

headers = { "Authorization": f"Token {TOKEN}"}

def getSites():
    # Block of code gets all sites in the specified Org
    url = f"{API_URL}/orgs/{ORG_ID}/sites"                      # The API url used to get all sites in the org
    r = requests.request("GET", url, headers=headers)           # Placing the result in the variable, r
    return r.json()                                             # Returning the result in json format

def getClients(siteID):
    #Block of code gets all Connected clients in a site
    url = f"{API_URL}/sites/{siteID}/stats/clients"             # The API url used to get statistics of clients in a site
    r = requests.request("GET", url, headers=headers)           # Placing the result in the variable, r
    return r.json()                                             # Returning the result in json format
    
def main():
    sites = getSites()                                          # Placing the return from getSites() function into variable, sites
    totalClients = 0                                            # Initializing the variable with a zero integer

    timestamp = int(time.time() * 1000000000)                   # Getting timestamp in nanoseconds for InfluxDB

    for site in sites:                                          # Looping through each site
        # Block of code to get site ID
        siteID = site.get("id")                                 # Getting the Site ID and putting the result into the varialbe, siteID

        clients = getClients(siteID)                            # Calling getClients function and putting results into variable, clients
        for client in clients:
            totalClients += 1
            
    #print(int(totalClients))
    print(f"mist_client_summary,org_id={ORG_ID} total={totalClients} {timestamp}")
            
            

if __name__ == "__main__":
    main()
