import os
import re
import requests

VM_IP = os.environ.get("VM_IP", "192.168.122.213")
url = f"http://{VM_IP}?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f"

headers = {
    "User-Agent": "ft_bornToSec",
    "Referer": "https://www.nsa.gov/",
}

r = requests.get(url, headers=headers)
match = re.search(r"flag is : ([a-f0-9]{64})", r.text, re.IGNORECASE)
if match:
    print(f"Flag: {match.group(1)}")
else:
    print("Flag not found in response")
