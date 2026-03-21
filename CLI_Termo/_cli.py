'''
Para testar direto no VSCode o código main.py e poder debugar por aqui
Porque tentar testar e debugar direto pelo pyodide não é dada intuitivo
'''

import main
import re

def converter_html_str(output):
    output = re.sub('</br>','\n',output)
    return re.sub('<.*?>','',output)

if __name__ == '__main__':
    print(converter_html_str(main.init()))
    while True:
        entrada = input('->')
        print(converter_html_str(main.receber_input(entrada)))