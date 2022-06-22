import socket
import os
from threading import Thread
import ssl
import re
import mimetypes
import urllib.parse
import sqlite3




class Https(Thread):
    def __init__(self,host="127.0.0.1",port=443,cert=None,key=None,racine="./"):
        Thread.__init__(self)
        # [+] Initialisation.
        self.state = False
        self.racine = racine

        print("[+] Initialisation en cours...")
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        print("[+] Demande %s %d"%(host,port))

        # [+] Verification certificats
        if(os.path.exists(cert)==False or os.path.exists(key)==False):
            print("[!] Impossible de joindre le certificat...NOK")
            return
        print("[+] Certificats présent...OK")
        self.context.load_cert_chain(cert,key)

        # [+] Creation de la socket
        try:
            self.MainSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.MainSock.bind((host,port))
        except:
            print("[!] Liaison socket impossible ...NOK")
            return
        print("[+] Initialisation...OK")
        self.state=True
        return

    # [+] Run Methode class Threading
    def run(self):
        if self.state == False:
            print("[!] Etat incorrect...NOK")
            return

        print("[+] Lancement en cours...")
        self.MainSock.listen()
        SslSock = self.context.wrap_socket(self.MainSock,server_side=True,do_handshake_on_connect=True)
        print("[+] Serveur en attente de clients...OK")
        while True:
            try:
                con, addr = SslSock.accept()
                #print("[+] Nouveau client {}".format(con.getpeername()))
                client = ClientHttps(client=con,racine=self.racine)
                client.start()

            except ssl.SSLError as e:
                print("[!] Serveur message : Erreur de type SSL...NOK")
            except OSError:
                print("[!] Serveur message : Erreur de type de socket...NOK")
            except:
                print("[!] Serveur message : Erreur fatale...NOK")
                exit(-1)


class ClientHttps(Thread):
    def __init__(self,client=None,racine="./www"):
        Thread.__init__(self)
        self.client =client
        self.headers = {}
        self.data = None
        self.racine = racine
        self.requests= ["/app"]

    def run(self):
        print("[+] Nouveau client {} ".format(self.client.getpeername()))
        self.data_brut = self.client.recv(1500).decode("utf-8")
        self.data = self.data_brut.split('\r\n')
        m = re.search(r'(GET|POST)\s([^\s]+)\s([^(\r|\n)]+)',self.data[0])
        uri = method = version = None
        if m:
            method=m.group(1)
            uri=m.group(2)
            version=m.group(3)
            print("   [+] : {} {} {}".format(method,uri,version))
            self.headers = self.GetFormat()
            print(self.headers)
            # self.args = self.GetArgs()
            headers = {
                'Server:' : ' Aleuzla-Serveur',
                'Host:' : ' {}'.format(socket.gethostbyname(socket.gethostname())),
            }
            try:
                version = 'HTTP/1.1'

                if method=="POST" and uri in self.requests:
                    request = True
                    # [+] On demande une fonction particulière
                    print("[+] Demande de requetes identifiées %s"%(uri))
                    print("   [+] Longueur data, attendu {}".format(self.headers['Content-Length']))
                    body = b" \0"
                    m = re.search("\r\n(.+)$",self.data_brut)
                    # [+] On vérifie que la recherche est correcte
                    if m != None and len(m.group(1)) == int(self.headers['Content-Length']):
                        print("  [+] Vérification OK")
                        if uri == "/app":
                            print(urllib.parse.unquote(m.group(1)))

                    # [+] On demande un GET 
                if method=="GET":
                    f = open(self.racine+uri,'rb')
                    body = f.read()
                    f.close()

                headers['Content-Length:']= len(body)
                headers['Content-type:'] = '{}'.format(mimetypes.guess_type(uri+'; charset=UTF-8'))
                status = '200 OK'
            except OSError:
                print("   [!] Fichier introuvable ou illisible")
                body = b"404 FICHIER INTROUVABLE"
                headers['Content-Length:']= len(body)
                headers['Content-type:'] = 'application/txt; charset=UTF-8'
                status='404 Not Found'
            self.client.send(b'%s %s'%(version.encode('utf-8'),status.encode('utf-8')))
            for e in headers.keys():
                self.client.send('{}: {} \r\n'.format(e,headers[e]).encode('utf-8'))
            self.client.send(b'\r\n')
            self.client.send(body)
        self.client.close()


    def GetFormat(self):
        headers = {}
        # [+] Construction de l'headers
        for e in self.data:
            m = re.search(r'(.+):\s(.+)$',e)
            if m != None:
                headers[m.group(1)] = m.group(2)
        return headers
        # [+] Récupération




