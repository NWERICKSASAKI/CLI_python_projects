"""
Peguei literamente de um dicionário online palavras 5 letras
Colei num bloco de notas e salvei
Para retirar os caracteres especiais:
Rodei esse código.
"""

import unidecode

ARQUIVO = '5.txt'

with open(ARQUIVO, 'r', encoding='utf-8') as f:
    content = f.read()

content = unidecode.unidecode(content)

with open(ARQUIVO, 'w') as f:
    f.write(content)
