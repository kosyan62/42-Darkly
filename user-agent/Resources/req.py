import requests

url = "http://192.168.122.213?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f"

headers = {
    "User-Agent": "ft_bornToSec",
    "Referer": "https://www.nsa.gov/"
}

r = requests.get(url, headers=headers)
with open("response.html", "w") as f:
    f.write(r.text)
    
# flag is f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188