import socket,re,urllib.parse,pathlib,mimetypes,json,hashlib
import sqlite3
from threading import Thread

class Client(Thread):
    def __init__(self,sock,racine,db):
        Thread.__init__(self)
        self.headers = {}
        self.sock = sock
        self.data = None
        self.racince = racine
        self.db = db

        print("[+] Bienvenue à {}".format(sock.getpeername()))

    def run(self):
        self.data = self.sock.recv(1500).decode("utf-8")
        sdata = self.data.split('\r\n')

        # ================================================
        # [+] CONTENU DE LA REQUETE
        # ================================================
        m = re.search(r'(GET|POST)\s([^\s]+)\s([^(\r|\n)]+)',sdata[0])
        uri = method = version = contenu = None
        if m:
            method = m.group(1)
            uri = m.group(2)
            version = m.group(3)
            self.headers,contenu = self.GetHeader(sdata,self.data)
            print("   [+] %s %s %s"%(method,uri,version))
            for e in self.headers.keys():
                print("   [+] {}: {}".format(e,self.headers[e]))
            print("   [>] Contenu : {}".format(contenu))

        # ================================================
        # [+] CONSTRUCTION HEADERS POUR CLIENT
        # ================================================
        headers = {
            'Server:' : ' Aleuzla-Serveur',
            'Host:' : ' {}'.format(socket.gethostbyname(socket.gethostname())),
            'Accept-Language:': ' fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding:': 'gzip, deflate, br'
        }
        try:
        #contenu = urllib.parse.unquote(contenu)
        # ================================================
        # [+] VERIFICATION DE LA DEMANDE 
        # ================================================
            body,uri,headers = self.ExecCommand(method,uri,self.headers,contenu)
            if(body == None): body = pathlib.Path(self.racince+uri).read_bytes()

            headers['Content-Length:']= len(body)
            headers['Content-type:'] = '{}'.format(mimetypes.guess_type(uri)[0]+"; charset=UTF-8;")
            headers['Accept:'] = '{}'.format(mimetypes.guess_type(uri)[0]);
            status = '200 OK'
        except OSError as e:
            print(e)
        # ================================================
        # [+] ERROR DE LA PAGE
        # ================================================
            print("   [!] Fichier introuvable ou illisible")
            body = b"404 FICHIER INTROUVABLE"
            headers['Content-Length:']= len(body)
            headers['Content-type:'] = 'text/plain; charset=UTF-8;'
            headers['Accept:'] = 'text/plain'
            status='404 Not Found'
        # ================================================
        # [+] ENVOI DE LA DONNE AU CLIENT
        # =================================================
        # [+] On transmet les données au cmimetypes.guess_type(uri)lient.
        self.sock.send(b'%s %s\r\n'%('HTTP/2'.encode('utf-8'),status.encode('utf-8')))
        for e in headers.keys():
            self.sock.send('{}: {}\r\n'.format(e,headers[e]).encode('utf-8'))
        self.sock.send(b'\r\n')
        self.sock.send(body)
#        self.sock.send(b'\r\n')
        self.sock.close()


    def GetHeader(self,sdata,data):
        headers = {}
        # [+] Construction de l'headers et récupération du contenu de la page
        for e in sdata:
            m = re.search(r'(.+):\s(.+)$',e)
            if m != None:
                headers[m.group(1)] = m.group(2)
                # essayer (\r\n\r\n(.+)$)
                data = data.replace("{}\r\n".format(m.group(0)) ,'') 
        # On récuperer le contenu restant.
        m = re.search(r'\r\n\r\n(.+)$',data)
        if m != None:
            data = m.group(1)
#        print(data)
        return headers, data


# [+] Gestion des commandes envoyées
    def ExecCommand(self,method,uri,header,contenu):
        rheader = {}
        # [+] Demande authentification
        if uri=="/ident" and method=="POST":
        # =============================================
        # DEMANDE AUTHENTIFICATION
        # ============================================

            try:
                print("   [+] Verification authentification...OK")
                contenu = json.loads(contenu)
                # ======================================
                # HASH CONTENU
                # ======================================
                h = hashlib.sha256()
                login = contenu["login"]
                password = contenu["pass"].encode()
                h.update(password)
                password = h.hexdigest()
                print(password+ " " + login)
                rows = self.db.Query("SELECT * FROM admin WHERE login='{}' AND pass='{}'".format(login,password))
                if len(rows) == 1:
                    print("   [+] Demande authentification %s...OK"%(login))
                    rheader['Set-Cookie:'] = " IDENT={}:::{}; Secure; HttpOnly".format(login,password)
                    print("   [+] Demande cookies pour login  {}".format(login))
                    return b"succes","ident.html",rheader
            except sqlite3.Error as e:
                print(e)
                pass
        #contenu = urllib.parse.unquote(contenu)
            print("   [!] Demande authentification...NOK")
            return b"fail","ident.txt",rheader

        return None,uri,rheader