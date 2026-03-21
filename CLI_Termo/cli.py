import main
import re
# Para DEBUGAR ~~~ pq só rodar no navegador (pyodide) é impossível

def converter_html_str(output):
    output = re.sub('</br>','\n',output)
    return re.sub('<.*?>','',output)

# def args(*args):
#     print(list(*args))

# if __name__ == '__main__':
#     args('oi')
#     args('a','e')
#     args(['a','o'])

if __name__ == '__main__':
    print(converter_html_str(main.init()))
    while True:
        entrada = input('->')
        print(converter_html_str(main.receber_input(entrada)))