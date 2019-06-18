import requests, sys

server = "http://rest.ensembl.org"


def chromo(species, number):

    ext3 = "/info/assembly/"
    spcs = species
    nmbr = str(number)
    t = requests.get(server + ext3 + spcs + '/' + nmbr, headers={"Content-Type": "application/json"})

    if not t.ok:
        t.raise_for_status()
        sys.exit()

    decoded = t.json()
    return decoded['length']

print(chromo('homo sapiens', '2'))