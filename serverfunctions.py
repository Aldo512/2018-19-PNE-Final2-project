import requests, sys

server = "http://rest.ensembl.org"

def countsp(*args):

    ext = "/info/species?"
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

#_____________________________________________________________________________________________

def kary(spcname):

    spcname = spcname.replace('+', '_')

    ext2 = "/info/assembly/homo_sapiens?"
    spc = ext2[0:ext2.find('y')+2] + spcname
    s = requests.get(server + spc, headers={"Content-Type": "application/json"})

    if not s.ok:
        s.raise_for_status()
        sys.exit()

    decoded = s.json()
    return decoded

#__________________________________________________________________________________________________

def chromo(species,number):

    ext3 = "/info/assembly/"
    spcs = species.replace('%20', ' ')
    nmbr = str(number)
    t = requests.get(server + ext3 + spcs + '/' + nmbr, headers={"Content-Type": "application/json"})

    if not t.ok:
        t.raise_for_status()
        sys.exit()

    decoded = t.json()
    return decoded['length']

#_________________________________________________________________________________________________________

def geneseq(gen):

    ext4 = '/homology/symbol/human/'
    gene = gen
    u = requests.get(server + ext4 + gene, headers={"Content-Type": "application/json"})

    if not u.ok:
        u.raise_for_status()
        sys.exit()

    decoded = u.json()
    return decoded['data'][0]['homologies'][0]['target']['align_seq']

#___________________________________________________________________________________________________________

def geneinfo(symbol):

    if symbol.find('ENG') != -1:

        return 'Error. Enter a valid gene symbol'

    ext5 = "/xrefs/symbol/homo_sapiens/"
    symb = symbol

    r = requests.get(server + ext5 + symb, headers={"Content-Type": "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    decoded = r.json()
    smbl= decoded[0]['id']

    ext6 = "/lookup/id/"

    s = requests.get(server + ext6 + smbl, headers={"Content-Type": "application/json"})

    if not s.ok:
        s.raise_for_status()
        sys.exit()

    infor = s.json()

    ext7 = "/sequence/id/"

    codons = requests.get(server + ext7 + smbl, headers={"Content-Type": "text/plain"})

    if not codons.ok:
        codons.raise_for_status()
        sys.exit()

    return infor['seq_region_name'], infor['start'], infor['end'], smbl, codons.text

#_______________________________________________________________________________________________________

def genecalc(gne):

    data =geneinfo(gne)

    As = data[4].upper().count('A')
    Ts = data[4].upper().count('T')
    Cs = data[4].upper().count('C')
    Gs = data[4].upper().count('G')
    total = As+Cs+Ts+Gs

    PrA = round((As/total)*100, 2)
    PrT = round((Ts/total)*100, 2)
    PrC = round((Cs/total)*100, 2)
    PrG = round((Gs/total)*100, 2)

    return As, Ts, Cs, Gs, total, PrA, PrT, PrC, PrG

#___________________________________________________________________________________________________________

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
