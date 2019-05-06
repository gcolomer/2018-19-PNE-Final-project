import http.server
import socketserver
import termcolor
import json
import http.client
from Seq import Seq

# Define the Server's port
PORT = 8000


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):
    def diccionario_split(self, path):
        diccionario = dict()
        if '?' in self.path:
            dicc = self.path.split("?")[1]
            dicc = dicc.split(" ")[0]
            trozos = dicc.split("&")
            for pareja in trozos:
                if '=' in pareja:
                    key = pareja.split("=")[0]
                    value = pareja.split("=")[1]
                    diccionario[key] = value
        return (diccionario)

    def do_GET(self):
        response_code = 200
        json_response = False

        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # IN this simple server version:
        # We are NOT processing the client's request
        # It is a happy server: It always returns a message saying
        # that everything is ok

        # Message to send back to the client
        if self.path == "/":
            with open("index.html", "r") as f:
                contents = f.read()
        # here we read the index.html code.
        elif "listSpecies" in self.path:
            dicc = self.diccionario_split(self.path)
            if 'limit' in dicc:
                try:
                    limit = int(dicc['limit'])
                except:
                    limit = 0
            else:
                limit = 0

            conn = http.client.HTTPConnection('rest.ensembl.org')
            conn.request("GET", "/info/species?content-type=application/json")
            r1 = conn.getresponse()

            # -- Print the status
            print()
            print("Response received: ", end='')
            print(r1.status, r1.reason)

            # -- Read the response's body and close
            # -- the connection
            text_json = r1.read().decode("utf-8")
            response = json.loads(text_json)
            print(response)

            species = response['species']
            if 'json' in dicc and dicc['json'] == '1':
                json_response = True
                if limit == 0:
                    limit = len(species)
                newlist = species[1:limit]
                contents = json.dumps(newlist)
            else:
                if limit == 0:
                    limit = len(species)

                print("Limit: ", limit)
                contents = """
                                        <html>
                                        <body style ="background-color: salmon;">
                                        <ul> """

                cont = 0
                for specie in species:
                    contents = contents + "<li>" + specie['display_name'] + "</li>"
                    cont = cont + 1
                    print(cont, limit)
                    if (cont == limit):
                        break

                contents = contents + """<ul>
                                        <body>
                                        <html>
                                        """

            conn.close()


        elif "karyotype" in self.path:
            dicc = self.diccionario_split(self.path)
            if 'specie' in dicc and dicc['specie'] != '':
                specie = dicc['specie']
                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/info/assembly/" + specie + "?content-type=application/json")
                r1 = conn.getresponse()
                text_json = r1.read().decode("utf-8")
                response = json.loads(text_json)
                print(response)
                if 'karyotype' in response:
                    list_chromo = response['karyotype']
                    if 'json' in dicc and dicc['json'] == '1':
                        json_response = True
                        print(list_chromo)
                        contents = json.dumps(list_chromo)
                    else:
                        contents = """
                                    <html>
                                    <body style ="background-color: salmon;">
                                    <ul> """

                        for chromo in list_chromo:
                            contents = contents + "<li>" + chromo + "</li>"

                        contents = contents + """</ul>
                                    </body>
                                    </html>
                                    """
                else:
                    response_code = 400
                    f = open('Error.html', 'r')
                    contents = f.read()
            else:
                response_code = 400
                f = open('Error.html', 'r')
                contents = f.read()

        elif "chromosomeLength" in self.path:
            dicc = self.diccionario_split(self.path)
            if 'chromo' in dicc and 'specie' in dicc and dicc['chromo'] != '' and dicc['specie'] != '':
                chromo1 = dicc['chromo']
                specie = dicc['specie']
                print(chromo1)
                print(specie)
                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/info/assembly/" + specie + "?content-type=application/json")
                r1 = conn.getresponse()
                text_json = r1.read().decode("utf-8")
                response = json.loads(text_json)
                info = response['top_level_region']

                if 'json' in dicc and dicc['json'] == '1':
                    json_response = True
                    long = 0
                    for elemento in info:
                        if (elemento['name'] == chromo1):
                            long = elemento['length']
                    dic = dict()
                    dic['len'] = long
                    contents = json.dumps(dic)
                else:
                    long = 0
                    for elemento in info:
                        if (elemento['name'] == chromo1):
                            long = elemento['length']
                    contents = """
                                           <html>
                                           <body style ="background-color: salmon;">
                                           <ul> """

                    contents = contents + "<li>" + str(long) + "</li>"

                    contents = contents + """</ul>
                                            </body>
                                            </html>"""
            else:
                response_code = 400
                f = open('Error.html', 'r')
                contents = f.read()
        elif "geneSeq" in self.path:
            dicc = self.diccionario_split(self.path)
            if 'gene' in dicc and dicc['gene'] != '':

                gene = dicc['gene']

                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
                r1 = conn.getresponse()
                raw_data = r1.read().decode("utf-8")
                response = json.loads(raw_data)

                try:
                    id = response['data'][0]['id']
                    conn.request("GET", "/sequence/id/" + id + "?content-type=application/json")
                    r1 = conn.getresponse()
                    text_json = r1.read().decode("utf-8")
                    response = json.loads(text_json)
                    cadena = response['seq']

                    if 'json' in dicc and dicc['json'] == '1':
                        json_response = True

                        dic = dict()
                        dic['seq'] = cadena
                        contents = json.dumps(dic)
                    else:

                        contents = """
                                                           <html>
                                                           <body style ="background-color: salmon;">
                                                           <font face="garamond"  color = "black"</font>
                                                            </h4>This page provides information about the gene requested</h4>
                                                           <ul> """

                        contents = contents + "<ul>" + cadena + "<ul>"

                        contents = contents + """</ul>
                                                            </body>
                                                            </html>"""
                except KeyError:
                    response_code = 400
                    f = open('Error.html', 'r')
                    contents = f.read()
            else:
                response_code = 400
                f = open('Error.html', 'r')
                contents = f.read()

        elif "geneList" in self.path:
            dicc = self.diccionario_split(self.path)
            if 'start' in dicc and 'chromo' in dicc and 'end' in dicc and dicc['start'] != '' and dicc[
                'chromo'] != '' and dicc['end'] != '':
                start = dicc['start']
                chromo = dicc['chromo']
                end = dicc['end']

                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/overlap/region/human/" + str(chromo) + ":" + str(start) + "-" + str(
                    end) + "?content-type=application/json;feature=gene")
                r1 = conn.getresponse()
                data1 = r1.read().decode("utf-8")
                response = json.loads(data1)
                if 'error' in response:
                    response_code = 400
                    f = open('Error.html', 'r')
                    contents = f.read()
                else:
                    if 'json' in dicc and dicc['json'] == '1':
                        json_response = True
                        lista = []
                        counter = 0
                        ending = int(end)-int(start)

                        for item in response:
                            if 'feature_type' in item and item['feature_type'] == 'gene':
                                lista.append(item['external_name'])
                                counter = counter + 1
                                if counter == ending:
                                    break
                        dic = dict()
                        dic['Gene'] = lista

                        contents = json.dumps(dic)
                    else:
                        ending = int(end) - int(start)

                        contents = """
                                  <html>
                                  <body style ="background-color: salmon;">
                                  <font face="garamond"  color = "black"</font>
                                    </h3>This page shows all the genes asked in the form</h3>
                                   <ul>"""

                        counter = 0

                        for item in response:

                            if 'feature_type' in item and item['feature_type'] == 'gene':
                                contents = contents + '<li>' + item['external_name'] + '</li>'

                                counter = counter + 1

                                if counter == ending:
                                    break

                        contents = contents + """
                                     </ul>
                                    </body>
                                   </html>"""

            else:
                response_code = 400
                f = open('Error.html', 'r')
                contents = f.read()




















        elif "geneInfo" in self.path:
            dicc = self.diccionario_split(self.path)
            if 'gene' in dicc and dicc['gene'] != '':
                gene = dicc['gene']

                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
                r1 = conn.getresponse()
                raw_data = r1.read().decode("utf-8")
                response = json.loads(raw_data)
                try:
                    id = response['data'][0]['id']

                    conn.request("GET", "/overlap/id/" + id + "?feature=gene;content-type=application/json")
                    r1 = conn.getresponse()
                    raw_data = r1.read().decode("utf-8")
                    response = json.loads(raw_data)
                    start = response[0]['start']
                    end = response[0]['end']
                    id = response[0]['id']
                    lenght = end - start
                    chromo = response[0]['assembly_name']

                    if 'json' in dicc and dicc['json'] == '1':
                        json_response = True

                        dic = dict()
                        dic['id'] = id
                        dic['start'] = start
                        dic['end'] = end
                        dic['lenght'] = lenght

                        contents = json.dumps(dic)
                    else:

                        contents = """
                                                                         <html>
                                                                       <body style ="background-color: salmon;">
                                                                       <font face="garamond" size= 5 color = "black"</font>
                                                                        </h4>This page provides information about the gene requested</h4>
                                                                       <ul> """

                        contents = contents + "<h4>Id: <h4>" "<li>" + id + "</li>"
                        contents = contents + "<h4>Start: <h4>" "<li>" + str(start) + "</li>"
                        contents = contents + "<h4>End: <h4>" "<li>" + str(end) + "</li>"
                        contents = contents + "<h4>Lenght: <h4>" "<li>" + str(lenght) + "</li>"
                        contents = contents + "<h4>Chromosome:  <h4>""<li>" + chromo + "</li>"

                        contents = contents + """</ul>
                                                                        </body>

                                                                        </html>"""
                except KeyError:
                    response_code = 400
                    f = open('Error.html', 'r')
                    contents = f.read()
            else:
                response_code = 400
                f = open('Error.html', 'r')
                contents = f.read()

        elif "geneCal" in self.path:
            dicc = self.diccionario_split(self.path)
            if 'gene' in dicc and dicc['gene'] != '':
                gene = dicc['gene']
                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
                r1 = conn.getresponse()
                raw_data = r1.read().decode("utf-8")
                response = json.loads(raw_data)
                try:
                    id = response['data'][0]['id']
                    conn.request("GET", "/sequence/id/" + id + "?content-type=application/json")
                    r1 = conn.getresponse()
                    text_json = r1.read().decode("utf-8")
                    response = json.loads(text_json)
                    cadena = response['seq']

                    print("Sequence: " + cadena)
                    s1 = Seq(cadena)
                    total = len(cadena)
                    percA = s1.perc('A')
                    percT = s1.perc('T')
                    percG = s1.perc('G')
                    percC = s1.perc('C')
                    if 'json' in dicc and dicc['json'] == '1':
                        json_response = True

                        dic = dict()
                        dic['lenght'] = total
                        dic['percA'] = percA
                        dic['percT'] = percT
                        dic['percG'] = percG
                        dic['percC'] = percC

                        contents = json.dumps(dic)
                    else:

                        contents = """
                                                                                 <html>
                                                                                <body style ="background-color: salmon;">
                                                                                <font face="garamond" size= 5 color = "black"</font>
                                                                                </h4>This page provides information about the gene requested</h4>
                                                                                 <ul> """

                        contents = contents + "<h4>Lenght: <h4>" "<li>" + str(total) + "</li>"
                        contents = contents + "<h4>Percentage of A: <h4>" "<li>" + str(percA) + "</li>"
                        contents = contents + "<h4>Percenatge of T: <h4>" "<li>" + str(percT) + "</li>"
                        contents = contents + "<h4>Percenatge of G: <h4>" "<li>" + str(percG) + "</li>"
                        contents = contents + "<h4>Percenatge of C:  <h4>""<li>" + str(percC) + "</li>"

                        contents = contents + """</ul>
                                                                                      </body>

                                                                                      </html>"""
                except KeyError:
                    response_code = 400
                    with open("error.html", "r") as f:
                        contents = f.read()
            else:
                response_code = 400
                with open("error.html", "r") as f:
                    contents = f.read()

        else:
            response_code = 404
            with open("error.html", "r") as f:
                contents = f.read()

        # Generating the response message
        self.send_response(response_code)  # -- Status line: OK!
        if (json_response == True):
            # Define the content-type header:
            self.send_header('Content-Type', 'application/json')
        else:
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
socketserver.TCPServer.allow_reuse_address = True

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
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