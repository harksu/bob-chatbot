import requests
import os
from dotenv import load_dotenv

load_dotenv()

ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")

#https://docs.abuseipdb.com/#configuring-fail2ban test code 
def abuseipdb_query(ip_address):
    print("abuseipdb_query called with", ip_address)
    url = "https://api.abuseipdb.com/api/v2/check"
    querystring = {
        "ipAddress": ip_address,
        "maxAgeInDays": "30"  
    }
    headers = {
        "Accept": "application/json",
        "Key": ABUSEIPDB_API_KEY
    }
    response = requests.request(method="GET", url=url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}
