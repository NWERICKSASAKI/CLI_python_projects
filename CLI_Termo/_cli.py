'''
Para testar direto no VSCode o código main.py e poder debugar por aqui
Porque tentar testar e debugar direto pelo pyodide não é dada intuitivo

P.S: Não vai aparacer as letras coloridas porque retirei o Colorama.
'''

import main
import re

def converter_html_str(output):
    output = re.sub('<br>','\n',output)
    return re.sub('<.*?>','',output)

if __name__ == '__main__':
    termo:main.Termo = main.init()
    print(converter_html_str(main.output))

    while True:
        entrada = input('->')
        response = main.termo.inserir_input(entrada)
        print(converter_html_str(main.output))