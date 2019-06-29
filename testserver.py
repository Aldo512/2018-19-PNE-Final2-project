import requests, sys

server = "http://rest.ensembl.org"
ext = "/sequence/id/ENSG00000165879?"

r = requests.get(server + ext, headers={"Content-Type": "text/plain"})

if not r.ok:
    r.raise_for_status()
    sys.exit()

print(len(r.text))
