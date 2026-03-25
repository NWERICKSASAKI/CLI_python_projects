output:str = ''

lista_opcoes = ['CLI (simula um termina de python)',
                'Termo (sim, o jogo)',
                'Scoundrel (um jogo de carta adaptado)'
                ]

lista_numeros_em_string = ['zero','um','dois','tres','quatro','cinco','seis','sete','oito','nove','dez']

def exibir_opcoes():
    global lista_opcoes
    texto:str = ''
    for idx, projeto in enumerate(lista_opcoes, start=1):
        texto += f'{idx} - {projeto}\n'
    return texto    

def exibir_tela():
    global output
    output = f'''<span style="white-space: pre-line;">
        Bem vindo aos meus projetos de CLI em Python,
        Digite um número e dê [ENTER]:
        
        {exibir_opcoes()}
                
        Por enquanto é só isso, vou acrescentando mais coisa futuramente.     
        - NWErickSasaki
        </span><br>'''

def recebe_input(entrada_usuario:str) -> int:
    exibir_tela()
    n = valida(entrada_usuario)
    return n
    

def valida(entrada:str) -> int:
    '''Recebe um número, caso bata com a opção, retorna ele.;7'''
    global output
    if not entrada.isnumeric():
        if entrada.lower() in lista_numeros_em_string:
            output += f'<span style="color: red">❌ A opção "{entrada}" até pode representar um número, MAS EU QUERO SÓ O NÚMERO SEM LETRAS!!!</span>'
        else:
            output += f'<span style="color: red">❌ A opção "{entrada}" contém letras, quero só números...</span>'
        return 0
    n = int(entrada)
    if 0 < n <= len(lista_opcoes):
        output += f'<span style="color: green">✅ Transferindo você!</span>'
        return n
    output += f'<span style="color: red">❌ A opção "{entrada}" não está entre as opções válidas...</span>'
    return 0

if __name__ == '__main__':
    exibir_tela()
