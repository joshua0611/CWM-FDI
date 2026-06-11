"""
SQL injection attack pentester.

Searches for input fields in the form of a site, posts singular inverted commas into the forms. Tries to do so for all input fields in case of checks on incomplete forms. Seeks out only forms with post actions.

Looks for error codes over 500 and reports them, with relevant input delivered.
"""

import string
import time
import requests
from bs4 import BeautifulSoup
import httplib2

URL      = "http://127.0.0.1:5000/login"
USERNAME = "admin"
SAMPLES  = 5         # measurements per candidate — increase if signal is noisy
CHARSET  = string.ascii_lowercase + string.digits

def main():
    data=get_data()
    for action in data.keys():
        print(f"Testing action: {action}")
        payload=generate_payload(data[action])
        results=test_payload(URL, payload)
        if results[0]:
            print(f"    VULNERABLE: striking form {action} caused error code {results[1]}")
        else:
            print(f"    SECURE, striking form {action} caused response code {results[1]}")

def get_data():
    h = httplib2.Http('.cache')
    response, content = h.request(URL)
    forms = BeautifulSoup(content, 'lxml').find_all('form')

    # Characterising forms in HTML
    data={} #forms[action]=[input.name for input in inputs]
    
    for form in forms:
        method=form.get('method')
        action=form.get('action')
        if method == 'POST':
            data[action]=[field.get('name') for field in form.select('input')]
    return data

def generate_payload(fields):
    """
    Takes as input a list of fields of a given form, and generates a list of data payloads (dicts)     containing SQL injection pentest loads of form {"name":" ' ", etc.} to be posted 
    """
    warhead=" ' " # SQL warhead to inject
    payload={target:warhead for target in fields}
    return payload

def test_payload(URL, payload):
    """
    Fires payload and checks for vulnerability.
 
    Takes as input a URL, and a payload (a dict containing {form_name:SQL_payload})

    Returns [vuln_flag, response_code], the former being a bool denoting vulnerability
    """
    resp=requests.post(URL, data=payload).status_code
    vuln_flag=bool(resp>=500)
    return [vuln_flag, resp]



def measure(password: str) -> float:
    """Return the average response time (seconds) for a login attempt."""
    total = 0.0
    for _ in range(SAMPLES):
        start = time.perf_counter()
        requests.post(URL, data={"username": USERNAME, "password": password})
        total += time.perf_counter() - start
    return total / SAMPLES

if __name__ == "__main__":
    main()
