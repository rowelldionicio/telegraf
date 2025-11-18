import requests
import os
import time
from urllib.parse import urljoin								# URL manipulation - for handling relative/absolute paths

API_URL = 'https://api.mist.com/api/v1'                         # API URL will change depending on your global 
TOKEN = os.getenv("<ENTER YOUR TOKEN ENV")                      # Calling an environment variable
ORG_ID = '<ENTER YOUR ORG ID>'                                  # Add in the org ID

headers = { "Authorization": f"Token {TOKEN}"}

# Get all clients in an org from the last 60 minutes of associations
def getAllClients(duration="60m"):
    url = f"{API_URL}/orgs/{ORG_ID}/clients/search"
    params = {"duration": duration, "limit": 1000}				# Query parameters with 1000 results per page

    allClients = []
	
    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        allClients.extend(data.get("results", []))

        # After the first request, follow the 'next' URL directly.
        next_url = data.get("next")
        if next_url:
            # If it's a relative URL, join it with the base URL
            if next_url.startswith('/'):
                url = urljoin('https://api.mist.com', next_url)
            else:
                # If it's absolute, use it as-is
                url = next_url
        else: 
            url = None
        
        params = None
    
    return allClients

def main():
    # Protocol counters
    beTotal = 0
    axTotal = 0
    acTotal = 0
    nTotal = 0
    gTotal = 0
    bTotal = 0
    aTotal = 0
    otherTotal = 0

    # Band counters
    totalBand24 = 0
    totalBand5 = 0
    totalBand6 = 0
    totalBandOther = 0

    clients = getAllClients(duration="60m")

    # Use a set to count unique MAC addresses
    macs = {c.get("mac") for c in clients if c.get("mac")}
    totalClients = len(macs)

    # Counting protocols and bands used
    for client in clients:                                          
        protocol = client.get("protocol")
        if protocol:
            if protocol == "be":
                beTotal += 1
            elif protocol == "ax":
                axTotal += 1
            elif protocol == "ac":
                acTotal += 1
            elif protocol == "n":
                nTotal += 1
            elif protocol == "g":
                gTotal += 1
            elif protocol == "b":
                bTotal += 1
            elif protocol == "a":
                aTotal += 1
            else:
                otherTotal += 1
        
        band = client.get("band")
        if band:
            if band == "24":
                totalBand24 += 1
            elif band == "5":
                totalBand5 += 1
            elif band == "6":
                totalBand6 += 1
            else: 
                totalBandOther += 1

    timestamp = int(time.time() * 1000000000)

    print(f"mist_client_summary,org_id={ORG_ID} total_clients={totalClients},be_total={beTotal},ax_total={axTotal},ac_total={acTotal},n_total={nTotal},g_total={gTotal},b_total={bTotal},a_total={aTotal},other_protocol_total={otherTotal},total_24={totalBand24},total_5={totalBand5},total_6={totalBand6},total_band_other={totalBandOther} {timestamp}")        
            

if __name__ == "__main__":
    main()
