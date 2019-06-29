import requests
import sys

server = "http://rest.ensembl.org"
ext = "/info/species?"
def countsp(*args):
    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    decoded = r.json()
    data = []

    if args:
        data.clear()
        spc = args[0]
        for i in range(spc):
            data.append(decoded['species'][i]['display_name'])

    else:
        spc = int(repr(decoded['species']).count('display_name'))
        data.clear()

        for i in range(len(decoded['species'])):
            data.append(decoded['species'][i]['display_name'])

    return data

print(countsp(10))