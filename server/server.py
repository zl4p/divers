#! /usr/bin/env python3

import socket,ssl,os,sqlite3
from sqlite3.dbapi2 import Error
from threading import Thread
from server_https import ClientHttps
from sql import DataBase
from client import Client

class server(Thread):
    def __init__(self,host="",port=443,key=None,cert=None,bdd="data.sqlite",racine="./"):
        self.context=None
        self.state = False
        self.MainBdd = None
        self.MainSock = None
        self.racine = racine

        Thread.__init__(self)
        print("[+] Initialisation en cours...OK")
# [+] Verification du protocole SSL + socket + bdd
        try:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.context.load_cert_chain(cert,key)

            self.MainSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.MainSock.bind((host,port))

            self.MainBdd = DataBase(bdd)

            self.state = True

        except sqlite3.Error:
            print("[!] Problème avec la base de données...NOK")
            return
        except ssl.SSLError as e:
            print("[!] Problème avec le certificat...NOK")
            print("   {}".format(e))
            return
        except OSError:
            print("[!] Probleme de création de socket...NOK")
        except SyntaxError as e:
            print("[!] Erreur fatale...NOK")
            print(e)
            exit(-1)
        print("   [+] Serveur pret pour %s %d"%(host,port))



# ============================================================
# [+] Lancement du thread
# ============================================================
    def run(self):
        if self.state == False:
            print("[!] Le serveur n'est pas pret...NOK")
            return
        
        self.MainSock.listen()
        SslSock = self.context.wrap_socket(self.MainSock,server_side=True,do_handshake_on_connect=True)
        print("[+] Serveur en attente de clients....OK")
        while True:
            try:
                con, addr = SslSock.accept()
                client = Client(sock=con,racine=self.racine,db=self.MainBdd)
                client.start()

            except ssl.SSLError as e:
                print("[!] Problème avec le certificat...NOK")
                print("   {}".format(e))
            except OSError:
                print("[!] Probleme de création de socket...NOK")
            except:
                print("[!] Process serveur erreur fatal...NOK")
                return
