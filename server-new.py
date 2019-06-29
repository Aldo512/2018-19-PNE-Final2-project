import http.server
import socketserver
import termcolor
import requests
import sys
# Server port at 8080
PORT = 8080

htmlheader = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">'''
htmlend = '''</body>
</html>'''

titlespcs = '''    <title>List of species</title>
</head>
<body style="background-color: yellow">'''

titlekar = '''    <title>Karyotype</title>
</head>
<body style="background-color: lightblue">'''

titlechromol= '''    <title>Chromosome length</title>
</head>
<body style="background-color: magenta">'''

titlegenesq = '''    <title>Gene sequence</title>
</head>
<body style="background-color: orange">'''

titlegeneinfo =  '''    <title>Gene sequence</title>
</head>
<body style="background-color: gold">'''

titlegenecalc = '''    <title>Gene sequence</title>
</head>
<body style="background-color: olive">'''
#_________________________Counting species______________________________

server = "http://rest.ensembl.org"
ext = "/info/species?"

#________________________Request for species________________________________


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

#___________________________/\/\/\/\_____________________________________


#________________________Request for karyotype___________________________

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

#_________________________/\/\/\/\/\_______________________________________


#________________________Request for chromosomes___________________________

def chromo(species, number):

    ext3 = "/info/assembly/"
    spcs = species.replace('%20', ' ')
    nmbr = str(number)
    t = requests.get(server + ext3 + spcs + '/' + nmbr, headers={"Content-Type": "application/json"})

    if not t.ok:
        t.raise_for_status()
        sys.exit()

    decoded = t.json()

    return decoded['length']

#_______________________/\/\/\/\/\/\/\_______________________________________


#_____________________Request for gene sequence_____________________________________

def geneseq(gen):

    ext4 = '/homology/symbol/human/'
    gene = gen
    u = requests.get(server + ext4 + gene, headers={"Content-Type": "application/json"})

    if not u.ok:
        u.raise_for_status()
        sys.exit()

    decoded = u.json()
    return decoded['data'][0]['homologies'][0]['target']['align_seq']

#_______________________/\/\/\/\/\/\/\___________________________________________


#________________________Request for gene information_____________________________

def geneinfo(symbol):

    if symbol.find('ENG') != -1:

        return 'Error. Enter a valid gene symbol'

    ext = "/xrefs/symbol/homo_sapiens/"
    symb = symbol

    r = requests.get(server + ext + symb, headers={"Content-Type": "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    decoded = r.json()
    smbl= decoded[0]['id']

    ext2 = "/lookup/id/"

    s = requests.get(server + ext2 + smbl, headers={"Content-Type": "application/json"})

    if not s.ok:
        s.raise_for_status()
        sys.exit()

    infor = s.json()

    ext3 = "/sequence/id/"

    codons = requests.get(server + ext3 + smbl, headers={"Content-Type": "text/plain"})

    if not codons.ok:
        codons.raise_for_status()
        sys.exit()

    return infor['seq_region_name'], infor['start'], infor['end'], smbl, codons.text

#_____________________________/\/\/\/\/\/\/\__________________________________________________


#____________________________Request for gene calculations____________________________________

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

#____________________________/\/\/\/\/\/\/\/\/\_______________________________________________
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        termcolor.cprint(self.requestline, 'green')

        # Message to send back to the client
        rqst = self.requestline.split(' ')
        got = rqst[1]
        dict1 = {'/': 'Index.html', '/Index.html': 'Index.html', '/lele': 'lele.html', '/listSpecies': 'listSpecies.html',
                 '/karyotype': 'Karyotype.html', '/chromosomeLength': 'Chromosome.html', '/favicon.ico': 'favicon.ico',
                 '/geneSeq': 'geneseq.html', '/geneInfo': 'geneInfo.html', '/geneCalc': 'geneCalc.html'}
        print(got)

        try:

            if got not in dict1:
                docu = open('Error.html')
                contents = docu.read()
                docu.close()

            if got.find('listSpecies?') == True:



                if got[got.find('=')] != got[-1]:
                    datacnt = int(got[got.find('=')+1:])

                    try:
                        data = countsp(datacnt)

                    except IndexError:
                        data = countsp()
                else:
                    data = countsp()

                lstnm = 1
                docu = open('Results.html', 'w+')
                docu.write(htmlheader + '\n' + titlespcs)

                for i in data:
                    docu.write(str(lstnm) + '. ')
                    docu.write(i)
                    docu.write('\n')
                    docu.write('</br>')
                    lstnm += 1

                docu.write('<a href="Index.html">Main menu</a>')
                docu.write(htmlend)
                docu.close()
                docu = open('Results.html', 'r')
                contents = docu.read()
                docu.close()

            elif got.find('karyotype?') == True:

                if got[-1] != '=':

                    docu = open('Karyoresults.html', 'w+')
                    lstnm = 1
                    docu.write(htmlheader)
                    decoding = kary(got[got.find('=')+1:])
                    docu.write('Results for chromosome names in: ' + got[got.find('=')+1:].replace('+', ' ') + '</br></br>')
                    decoded = decoding['karyotype']
                    docu.write(titlekar)

                    for i in decoded:
                        docu.write(str(lstnm) + '. ')
                        docu.write(i)
                        docu.write('\n')
                        docu.write('</br>')
                        lstnm += 1

                    docu.write('<a href="Index.html">Main menu</a>')
                    docu.write(htmlend)
                    docu.close()
                    docu = open('Karyoresults.html', 'r')

                else:
                    docu = open('Error.html', 'r')

                contents = docu.read()
                docu.close()

            elif got.find('chromosomeLength?') == True:

                got = got.replace(';', '&')
                termcolor.cprint(got, 'magenta')

                chrm = got[got.find('=')+1:got.find('&')].replace('+', ' ')
                chrnmr = got[got.find('chromo=') + 7:]
                infor = chromo(chrm, chrnmr)
                docu = open('Chromoresults.html', 'w+')
                docu.write(htmlheader)
                docu.write(titlechromol)
                docu.write(str(chrm + ' ' + '</br>' + 'chromosome: ' + chrnmr) + '</br>')
                docu.write('chromosome length: ' + str(infor))
                docu.write('</br> <a href="Index.html">Main menu</a>')
                docu.write(htmlend)
                docu.close()
                docu = open('Chromoresults.html', 'r')
                contents = docu.read()
                docu.close()

            elif got.find('geneSeq?') == True:

                got = got.replace(';', '&')
                gene = got[got.find('=')+1:]
                infor = geneseq(gene)
                docu = open('Seqresults.html', 'w+')
                docu.write(htmlheader)
                docu.write(titlegenesq)
                docu.write('Sequence returned for ' + gene + ':' + '\n' + '</br>')
                docu.write(infor)
                docu.write('\n' + '</br> <a href="Index.html">Main menu</a>')
                docu.write(htmlend)
                docu.close()
                docu = open('Seqresults.html', 'r')
                contents = docu.read()
                docu.close()

            elif got.find('geneInfo?') == True:

                gene = got[got.find('=') + 1:]
                docu = open('Inforesults.html', 'w+')
                inf = geneinfo(gene)
                docu.write(htmlheader)
                docu.write(titlegeneinfo)
                docu.write('Results for: ' + gene)
                docu.write('\n' + '</br>' + 'The gene is located in the chromosome: ' + str(inf[0]))
                docu.write('\n' + '</br>' + 'The gene is located between the bases number ' + str(inf[1]) + ' and ' + str(inf[2]))
                docu.write('\n' + '</br>' + 'The Ensembl id for the given gene is:  ' + str(inf[3]))
                docu.write('\n' + '</br>' + 'This gene has a length of: ' + str(len(inf[4])) + ' bases.')
                docu.write('\n' + '</br> <a href="Index.html">Main menu</a>')
                docu.write(htmlend)
                docu.close()
                docu = open('Inforesults.html', 'r')
                contents = docu.read()
                docu.close()

            elif got.find('geneCalc?') == True:

                gene = got[got.find('=') + 1:]
                docu = open('Calcresults.html', 'w+')
                docu.write(htmlheader)
                docu.write(titlegenecalc)
                data = genecalc(gene)
                docu.write('Showing results for: ' + gene + '\n' + '</br>')
                docu.write('The total amount of bases in the gene is: ' + str(data[4]) + '\n' + '</br>')
                docu.write('The total amount of As in the sequence are: ' + str(data[0]) + ' which corresponds to the ' + str(data[5]) + '%' + ' of the total bases' + '\n' + '</br>')
                docu.write('The total amount of Ts in the sequence are: ' + str(data[1]) + ' which corresponds to the ' + str(data[6]) + '%' + ' of the total bases' + '\n' + '</br>')
                docu.write('The total amount of Cs in the sequence are: ' + str(data[2]) + ' which corresponds to the ' + str(data[7]) + '%' + ' of the total bases' + '\n' + '</br>')
                docu.write('The total amount of Gs in the sequence are: ' + str(data[3]) + ' which corresponds to the ' + str(data[8]) + '%' + ' of the total bases' + '\n' + '</br>')
                docu.write('<a href="Index.html">Main menu</a>')
                docu.write(htmlend)
                docu.close()
                docu = open('Calcresults.html', 'r')
                contents = docu.read()
                docu.close()

            if got in dict1:

                if got != '/' and got != '/Index.html':

                    docu = open(dict1[got], 'r')
                    contents = docu.read()
                    docu.close()

                elif got == '/' or got == '/Index.html':

                    docu = open('Index.html', 'r')
                    contents = docu.read()
                    docu.close()

                elif got.find('favicon.ico') == True:
                    il = 0

        except ValueError:

            docu = open('Error.html')
            contents = docu.read()
            docu.close()

        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    socketserver.TCPServer.allow_reuse_address = True

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()

print("")
print("Server Stopped")