#! /usr/bin/env python3


import server


ssl_cert="./certs/server.cert"
ssl_key= "./certs/server.key"


if __name__ == "__main__":
    #Serveur = server_https.Https(cert=ssl_cert,key=ssl_key)
    #Serveur.start()
    server = server.server(cert=ssl_cert,key=ssl_key,racine="../superviseur",host="127.0.0.1")
    server.start()
