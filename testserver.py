import requests, sys

server = "http://rest.ensembl.org"

def genelist(chromo, start, end):

    ext = "/overlap/region/human/"
    chromo = str(chromo)
    start = str(start)
    end = str(end)

    r = requests.get(server + ext + chromo + ':' + start + '-' + end + '?feature=gene', headers={"Content-Type": "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    decoded = r.json()

    return decoded

print(genelist(10,97319267,97321915))
