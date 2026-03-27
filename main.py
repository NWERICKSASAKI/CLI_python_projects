import json

output:str = ''
lista_opcoes:list = []

lista_numeros_em_string = ['zero','um','dois','tres','quatro','cinco','seis','sete','oito','nove','dez']

def exibir_opcoes():
    global output
    global lista_opcoes
    lista_opcoes = le_json_diretorios()
    texto:str = ''
    for idx, projeto in enumerate(lista_opcoes, start=1):
        texto += f'{idx} - {projeto}\n'
    return texto    

def exibir_tela():
    global output
    output = ''
    output += f'''<span style="white-space: pre-line;">
        Bem vindo aos meus projetos de CLI em Python,
        Digite um número e dê [ENTER]:
        
        {exibir_opcoes()}
                
        Planejo acrescentar mais projetinhos futuramente.     
        - NWErickSasaki
        </span><br>'''

def recebe_input(entrada_usuario:str) -> int:
    exibir_tela()
    n = valida(entrada_usuario)
    return n
    

def valida(entrada:str) -> str:
    '''Recebe um número, caso bata com a opção, retorna o nome da pasta'''
    global output
    if not entrada.isnumeric():
        if entrada.lower() in lista_numeros_em_string:
            output += f'<span style="color: red">❌ A opção "{entrada}" até pode representar um número, MAS EU QUERO SÓ O NÚMERO SEM LETRAS!!!</span>'
        else:
            output += f'<span style="color: red">❌ A opção "{entrada}" contém outros caracteres além de números...</span>'
        return ''
    n = int(entrada)
    if 0 < n <= len(lista_opcoes):
        output += f'<span style="color: green">✅ Transferindo você!</span>'
        return lista_opcoes[n - 1]
    output += f'<span style="color: red">❌ A opção "{entrada}" não está entre as opções válidas...</span>'
    return ''

def le_json_diretorios() -> list:
    global output
    with open("projetos.json", "r") as f:
        lista_opcoes = list(json.load(f))
        # output += f'<span style="color: green">✅ Arquivo de projetos lido com sucesso!<br>{lista_opcoes}</span>'
        return list(lista_opcoes)

if __name__ == '__main__':
    exibir_tela()

# py -m http.server