#! /usr/bin/env python3
# -*- coding: utf-8 -*-


# =========================================================================
# Name : convert.py
# Auteur : Sol1
# Commentaire : Convert file modle to HTML file, inspired by ASCIIDOC.
# =========================================================================


import sys
import re

# Entete du ficher HTML
footer="""
</div>
</body>
</html>
"""

header="""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modele documentation</title>
    <link rel="stylesheet" href="css/fonts.css">
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
<div class="conteneur">
"""

if __name__ == "__main__" :
    if len(sys.argv) != 3:
        print("[!] %s <file_to_convert> <nom_destination>"%(sys.argv[0]))
    else:
        try:
            conv = open(sys.argv[1],"r")
            dest = open("./docs/%s.html"%sys.argv[2],"w")
            dest.writelines(header)
            # Configuration section
            print("[+] Lecture en cours...")

            for line in conv.readlines():
                if line == "\n":
                    pass
                # Header and BackToLine
                line = re.sub(r'^\=\s(.+)\n',r'<h1>\1</h1>',line)
                line = re.sub(r'^\=\=\s(.+)\n',r'<h3>\1</h3>',line)
                line = re.sub(r'^\.$','<br>',line)

                # Code INLINE
                for r in re.finditer(r'\s`[^`]+`\s',line):
                    print(r.group(0))
                    t = re.sub(r'(^\s`|^`)',r" <code>",r.group(0))
                    t = re.sub(r'(`$|`\s$)',r"</code> ",t)
                    line = line.replace(r.group(0),t)

                # Bold
                for r in re.finditer(r'((\s\*|^\*)[^*][^*]+\*\s)',line):
                    #print(r.group(0))
                    t = r.group(0).replace(r.group(0),'<b>%s</b>'%(re.sub(r'(^\s\*|^\*)(.+)\*\s$',r'\2',r.group(0))))
                    line = line.replace(r.group(0)," %s "%(t))

                # Italic
                for r in re.finditer(r'((\s\_|^\_)[^\_][^\_]+\_\s)',line):
                    #print(r.group(0))
                    t = r.group(0).replace(r.group(0),'<i>%s</i>'%(re.sub(r'(^\s\_|^\_)(.+)\_\s$',r'\2',r.group(0))))
                    line = line.replace(r.group(0)," %s "%(t))

                # 

                dest.write(line)
            dest.write(footer)
            dest.close()
            conv.close()
            print("[+] Fin de la lecture.")
        except IOError:
            print("[!] Impossibe d'ouvrir le fichier.")
            exit(-1)
