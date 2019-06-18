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

spctitle = '''    <title>List of species</title>
</head>
<body style="background-color: yellow">'''
#_________________________Counting species______________________________

server = "http://rest.ensembl.org"
ext = "/info/species?"

#________________________Request for species________________________________
data = []
def countsp(*args):
    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    decoded = r.json()

    if args:
        spc = args[0]

    else:
        spc = int(repr(decoded['species']).count('display_name'))

    for spec in range(spc):
        data.append(decoded['species'][spec]['display_name'])

    return decoded

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

#_______________________/\/\/\/\/\/\/\_____________________________________
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        termcolor.cprint(self.requestline, 'green')

        # Message to send back to the client
        rqst = self.requestline.split(' ')
        got = rqst[1]
        dict1 = {'/': 'Index.html', '/Index.html': 'Index.html', '/lele': 'lele.html', '/listSpecies': 'Species.html', '/karyotype': 'Karyotype.html', '/chromosomeLength': 'Chromosome.html', '/favicon.ico': 'favicon.ico'}
        print(got)

        try:

            if got not in dict1:
                docu = open('Error.html')
                contents = docu.read()
                docu.close()

            if got.find('listSpecies?') == True:

                data.clear()
                datacnt = 0

                if got[got.find('=')] != got[-1]:
                    datacnt = int(got[got.find('=')+1:])

                    try:
                        countsp(datacnt)

                    except IndexError:
                        data.clear()
                        countsp()
                else:
                    countsp()

                lstnm = 1
                docu = open('Results.html', 'w+')

                for i in data:
                    docu.write(str(lstnm) + '. ')
                    docu.write(i)
                    docu.write('\n')
                    docu.write('</br>')
                    lstnm += 1

                docu.write('<a href="Index.html">Main menu</a>')
                docu.close()
                docu = open('Results.html', 'r')
                contents = docu.read()
                docu.close()

            elif got.find('karyotype?') == True:

                docu = open('Karyoresults.html', 'w+')
                lstnm = 1

                if got[-1] != '=':
                    decoding = kary(got[got.find('=')+1:])
                    docu.write('Results for ' + got[got.find('=')+1:].replace('+', ' ') + '</br>')

                else:
                    decoding = kary('homo_sapiens')
                    docu.write('Results for Homo Sapiens </br>')

                decoded = decoding['karyotype']


                for i in decoded:

                    docu.write(str(lstnm) + '. ')
                    docu.write(i)
                    docu.write('\n')
                    docu.write('</br>')
                    lstnm += 1

                docu.write('<a href="Index.html">Main menu</a>')
                docu.close()
                docu = open('Karyoresults.html', 'r')
                contents = docu.read()
                docu.close()

            elif got.find('Chromolength') == True:

                chrm = got[got.find('=')+1:got.find('&')].replace('+', ' ')
                chrnmr = got[got.find('chromosome') + 11:]
                termcolor.cprint(chrm + chrnmr, 'yellow')
                infor = chromo(chrm, chrnmr)
                docu = open('Chromoresults.html', 'w+')
                docu.write(str(chrm + ' ' + chrnmr) + '</br>')
                docu.write(str(infor))
                docu.write('</br> <a href="Index.html">Main menu</a>')
                docu.close()
                docu = open('Chromoresults.html', 'r')
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