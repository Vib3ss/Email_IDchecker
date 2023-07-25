import re
import dns.resolver
import requests

email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

class DisposableEmailError(Exception):
	pass

def sanity(eid):
    if re.match(email_pattern, eid):
        print("Email ID you put is correct for now, We're further Checking.")
        match = re.search(r'@(.+)', eid)
        if match:
            domain = match.group(1)
            return domain
        else:
            return None
    else:
        print("Email ID you put is not valid, please enter a correct email ID.")
        return None

def checker(domain):
    try:
        result = dns.resolver.resolve(domain, 'MX')
        print("Domain has a valid MX server.")
    except dns.resolver.NoAnswer:
        print(f"No MX records found for {domain}.")
    except dns.resolver.NXDOMAIN:
        print(f"{domain} does not exist.")
    except dns.resolver.Timeout:
        print("DNS resolution timed out.")
    except dns.resolver.NoNameservers:
        print("No nameservers found.")


def disposable(eid):
    dis = requests.get(f"https://disposable.debounce.io/?email={eid}")
    data = dis.json()
    if "disposable" in data and data["disposable"] == "false":
        print("This is not a disposable email.")
    else:
        print("ERROR!!, This is a disposable email.")
        raise DisposableEmailError

eid = input("Enter your email ID:")
domain = sanity(eid)

if domain:
    checker(domain)
    try:
        disposable(eid)  # Call the disposable function after checking the domain
    except DisposableEmailError:
        print("Execution stopped due to a disposable email.")
