import bs4
import requests
import sys

if len(sys.argv) < 2:
    print("Usage: python main.py <domain> [!include_expired]")
    sys.exit(1)

domain = sys.argv[1]
include_expired = not (len(sys.argv) > 2)

def get_subdomains(domain, r=False):
    url = f"https://crt.sh/?identity=%.{domain}&sort=1" # search for subdomains and sort by newest
    if include_expired:
        url += f"&exclude=expired"
    if r: # reverse the sorting order
        url += f"&dir=^"
    else:
        url += f"&dir=v"
    response = requests.get(url)
    soop = bs4.BeautifulSoup(response.text, "html.parser")
    table = soop.find_all("table")[1]
    domains = []
    for row in table.find_all("tr"):
        td = row.find_all("td")
        if len(td) == 7:
            for d in td[5].decode_contents().split('<br/>'):
                d = d.strip()
                if d.startswith('*.'):
                    d = d[2:]
                if not d in domains:
                    domains.append(d)
    if 'Sorry, your search results have been truncated.' in response.text and not r:
        for d in get_subdomains(domain, True):
            if not d in domains:
                domains.append(d)
    return domains

for d in get_subdomains(domain):
    print(d)