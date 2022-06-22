import sqlite3
from sqlite3.dbapi2 import sqlite_version

initDB = [
'''
create table if not exists users (
    id integer primary key autoincrement,
    login text,
    pass text,
    ip text,
    session integer
);''',
'''
create table if not exists admin (
    id integer primary key autoincrement,
    login text,
    pass text,
    ip text,
    session integer
);
''' 
]
admin_name = "admin"
admin_pass = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

class DataBase:
    def __init__(self,bdd):
        self.bdd = bdd
        conn = sqlite3.connect(bdd)
        for e in initDB:
            conn.execute(e)
        conn.commit()
        #self.Query("INSERT INTO admin (login,pass,ip,session) VALUES('admin','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918','',0);")
    def Query(self,req):
        conn = sqlite3.connect(self.bdd)
        cur = conn.cursor()
        cur.execute(req)
        conn.commit()
        return cur.fetchall()