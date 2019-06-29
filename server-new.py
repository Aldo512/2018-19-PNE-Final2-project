import http.server
import socketserver
import termcolor
import serverfunctions
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

titlegeneinfo =  '''    <title>Gene info</title>
</head>
<body style="background-color: gold">'''

titlegenecalc = '''    <title>Gene calculations</title>
</head>
<body style="background-color: olive">'''

titlegenelist = '''    <title>Gene list</title>
</head>
<body style="background-color: teal">'''


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        termcolor.cprint(self.requestline, 'green')

        # Message to send back to the client
        rqst = self.requestline.split(' ')
        got = rqst[1]
        dict1 = {'/': 'Index.html', '/Index.html': 'Index.html', '/lele': 'lele.html', '/listSpecies': 'listSpecies.html',
                 '/karyotype': 'Karyotype.html', '/chromosomeLength': 'Chromosome.html', '/favicon.ico': 'favicon.ico',
                 '/geneSeq': 'geneseq.html', '/geneInfo': 'geneInfo.html', '/geneCalc': 'geneCalc.html', '/geneList': 'geneList.html'}
        print(got)

        try:

            if got not in dict1:
                docu = open('Error.html')
                contents = docu.read()
                docu.close()

            if got.find('listSpecies?') == True:

                countsp = serverfunctions.countsp

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

                kary = serverfunctions.kary

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

                chromo = serverfunctions.chromo
                got = got.replace(';', '&')
                termcolor.cprint(got, 'magenta')

                chrm = got[got.find('=')+1:got.find('&')].replace('+', ' ')
                chrnmr = got[got.find('chromo=') + 7:]
                infor = chromo(chrm,chrnmr)
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

                geneseq = serverfunctions.geneseq
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

                geneinfo = serverfunctions.geneinfo
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

                genecalc = serverfunctions.genecalc
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

            elif got.find('geneList?') == True:

                genelist = serverfunctions.genelist
                got = got.replace(';', '&')
                chromo = got[got.find('chromo')+7:got.find('start')-1]
                start = got[got.find('start')+6:got.find('end')-1]
                end = got[got.find('end')+4:]
                docu = open('Listresults.html', 'w+')
                docu.write(htmlheader)
                docu.write(titlegenelist)
                docu.write('Results shown for the given parameters: \n</br>Chromosome: ' + chromo + '\n</br>Start point: ' + start + '\n</br>Endpoint: ' + end + '\n</br></br>' + 'Genes in the given region: \n</br></br>')
                data = genelist(chromo,start,end)
                for i in range(len(data)):
                    docu.write(data[i]['external_name'] + '\n' + '</br>')
                docu.write('<a href="Index.html">Main menu</a>')
                docu.write(htmlend)
                docu.close()
                docu = open('Listresults.html', 'r')
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