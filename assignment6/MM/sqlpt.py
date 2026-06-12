"""
SQL injection attack pentester.

Searches for input fields in the form of a site, posts singular inverted commas into the forms. Tries to do so for all input fields in case of checks on incomplete forms. Seeks out only forms with post actions.

Looks for error codes over 500 and reports them, with relevant inputs and outputs delivered so vulnerable forms can be pinpointed.
"""

import string
import time
import requests
from bs4 import BeautifulSoup
import httplib2
from urllib.parse import urljoin
from pathlib import Path

# Initialising key variables
URL = "http://127.0.0.1:5000/joinAsClient"
baseline_test=True #Flag for whether to conduct baseline test

# Loading warheads
file_path = Path("warheads.txt")  # relative path
with file_path.open("r", encoding="utf-8") as f:
    warheads = [line.strip("\n").rstrip(",") for line in f if line.strip()]
    
# Loads baseline test warhead if baseline_test=true. Expects: payloads[action]={field_name: legal_payload}
if baseline_test:
    baseline_warheads = eval(Path("baseline.txt").read_text())

    

def main():
    print("schema: SECURE/VULNERABLE|action|response code|response time|<warhead tested>")
    data=get_data() 
    for action in data.keys():
        print(f"Testing action: {action}")
        payloads=generate_payloads(data[action], warheads)
        action_url=urljoin(URL, action)
        
        if baseline_test:
            start=time.perf_counter()
            results=test_payload(action_url, baseline_warheads[action])
            resp_time = str(round(time.perf_counter() - start, 3)) + "ms"
            print(f"    BASELINE|returned {results[1]}|took {resp_time}")
        else:
            pass
        
        for payload in payloads.keys():
            start=time.perf_counter()
            results=test_payload(action_url, payloads[payload])
            resp_time = str(round(time.perf_counter() - start, 3)) + "ms"
            warhead_text=payload[:5] + '...' if len(payload) > 75 else payload
            if results[0]:
                print(f"    VULNERABLE|returned {results[1]}|took {resp_time}|warhead: <{warhead_text}>")
            else:
                print(f"    SECURE|returned {results[1]}|took {resp_time}|warhead: <{warhead_text}>")

def get_data():
    h = httplib2.Http('.cache')
    response, content = h.request(URL)
    forms = BeautifulSoup(content, 'lxml').find_all('form')

    # Characterising forms in HTML
    data={} #forms[action]=[input.name for input in inputs]
    
    for form in forms:
        method=form.get('method')
        action=form.get('action')
        if method.upper() == 'POST':
            data[action]=[field.get('name') for field in form.select('input')]
    return data

def generate_payloads(fields, warheads):
    """
    Takes as input a list of fields of a given form, and generates a dict of data payloads (dicts)     containing SQL injection pentest loads of form payloads[warhead]={"name":[{warheads}], etc.} to be posted 
    """
    payloads={}
    for warhead in warheads:
        payload={target:warhead for target in fields}
        payloads[warhead]=payload
    return payloads

def test_payload(URL, payload):
    """
    Fires payload and checks for vulnerability.

    Takes as input a URL, and a payload (a dict containing {input_name:payload})
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
