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
URL = "http://127.0.0.1:5000/joinAsWorker"
baseline_test=True #Flag for whether to conduct baseline test

# Loading warheads
file_path = Path("warheads.txt")  # relative path
with file_path.open("r", encoding="utf-8") as f:
    warheads = [line.strip("\n").rstrip(",") for line in f if line.strip()]
    
# Loads baseline test warhead if baseline_test=true. Expects: payloads[action]={field_name: legal_payload}
if baseline_test:
    baseline_warheads = eval(Path("baseline_test.txt").read_text())



def main():
    print("schema: SAFE/VULN/BASE|action|response code|response time|page char length|page byte length|<warhead tested>")
    data=get_data() 
    for action in data.keys():
        print(f"Testing action: {action}")
        payloads=generate_payloads(data[action], warheads)
        action_url=urljoin(URL, action)
        
        if baseline_test:
            start=time.perf_counter()
            results=test_payload(action_url, baseline_warheads[action])
            resp_time = str(round(time.perf_counter() - start, 3)) + "ms"
            print(f"    BASE|{results[1]}|{resp_time}|{results[2]}|{results[3]}")
        else:
            pass
        
        for payload in payloads.keys():
            start=time.perf_counter()
            results=test_payload(action_url, payloads[payload])
            resp_time = str(round(time.perf_counter() - start, 3)) + "ms"
            warhead_text=payload[:5] + '...' if len(payload) > 75 else payload
            if results[0]:
                print(f"    VULN|{results[1]}|{resp_time}|{results[2]}|{results[3]}|warhead: <{warhead_text}>")
            else:
                print(f"    SAFE|{results[1]}|{resp_time}|{results[2]}|{results[3]}|warhead: <{warhead_text}>")

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
    Takes as input a list of fields and warheads, and generates a dict of data payloads (dicts) of form payloads[warhead]={"field1":warhead, "field2":warhead ...} to be posted 
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
    Returns [vuln_flag, response_code, response_char_length, response_byte_length], the former being a bool denoting vulnerability
    """
    resp=requests.post(URL, data=payload)
    resp_code=resp.status_code
    resp_charlen=len(resp.text)
    resp_bytelen=len(resp.content)
    vuln_flag=bool(resp_code>=500)
    return [vuln_flag, resp_code, resp_charlen, resp_bytelen]

if __name__ == "__main__":
    main()
