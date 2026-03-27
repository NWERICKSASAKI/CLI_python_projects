'''Gera um arquivo JSON com os nomes das pastas do diretório atual.
    Exclusivo pra mim (desenvolvedor que colocou está pagina online)'''

import os
import json

pastas:list = []

for nome in os.listdir('.'):
    if os.path.isdir(nome):
        if not '.' in nome:
            pastas.append(nome)

with open("projetos.json", "w") as f:
    json.dump(pastas, f)
