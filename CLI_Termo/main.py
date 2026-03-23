import random
from unidecode import unidecode


output:str=''

def print(*args, classe:str='', sep:str=' ', end:str='\n', insert_tag=True) -> None:
    '''
    Sobrepor a função original print() para converter todo output original
    por uma saída HTML.
    '''
    global output

    new_output = ''
    if len(args) == 0:
        new_output = end            
    else:
        string = str(args[0])
        if len(args)>1:
            string = sep.join(args)

        if classe:
            classe = f' class={classe}'

        if insert_tag:
            new_output = f'<span{classe}>{string}</span>{end}'
        else:
            new_output = f'{string}{end}'

    output += new_output.replace('\n', '<br>')
    return

def cls():
    global output
    output = ''

class Letra:
    def __init__(self, pos:int, palavra_resposta:str, letra_chutada=""):
        self.pos:int = pos
        self.palavra_resposta:str = unidecode(palavra_resposta)
        self.letra_chutada:str = letra_chutada.lower()
        self.letra_resposta:str = palavra_resposta[pos]
        self.letra_resposta_unicode:str = unidecode(self.letra_resposta)
        self.cor = self.atribuir_cor()

    def atribuir_cor(self):
        if self.letra_chutada == self.letra_resposta_unicode:
            return 'VERDE'
        elif self.letra_chutada in self.palavra_resposta:
            return 'AMARELO'
        else:
            return 'BRANCO'

    def __str__(self):
        if self.letra_chutada == self.letra_resposta_unicode:
            return f"<span class={self.cor}>{self.letra_resposta}</span>"
        return f"<span class={self.cor}>{self.letra_chutada}</span>"



class Termo:
    def __init__(self, seed:int=0, max_tentativas=5, n_letras:int=5):
        self._seed:int = seed
        self.max_tentativas = max_tentativas
        self.n_letras = n_letras
        self.tentativa = 0
        self.lista_palavras:list = self.ler_txt(f"{n_letras}.txt")
        self.palavra_da_rodada = ""
        self.exibicao:list[list] = []
        self.continuar = False

    def definir_seed(self, n:int):
        random.seed(n)
        self._seed = n

    def nova_rodada(self):
        numero_aleatorio:int = random.randrange(len(self.lista_palavras))
        self.palavra_da_rodada = self.lista_palavras.pop(numero_aleatorio)
        self.tentativa = 0
        self.exibicao:list[list] = []

    def exibir_tela(self):
        global output
        cls()
        print("- TERMO -", end='\n\n')
        for palavra in self.exibicao:
            # print(palavra, insert_tag=False)
            for letra in palavra:
                print(letra, end=' ', insert_tag=False)
            print()
        for i in range(self.max_tentativas - self.tentativa):
            print('_ '*self.n_letras)
        return output

    def entrada_tem_n_letras_certinho(self, entrada:str) -> bool:
        if not len(entrada)==self.n_letras:
            return False
        return True

    def nova_tentativa(self, entrada:str):
        if self.processar_palavra(entrada):
            return True
        self.tentativa += 1
        if self.tentativa == self.max_tentativas:
            return True
        return False

    def processar_palavra(self, palavra):
        letras_palavra = []
        for n, letra in enumerate(palavra):
            obj_letra = Letra(n, self.palavra_da_rodada, letra)
            letras_palavra.append(str(obj_letra))
        self.exibicao.append(letras_palavra)
        if palavra == unidecode(self.palavra_da_rodada):
            return True
        return False
    
    def encerrar(self):
        print(f"\nPalavra secreta: {self.palavra_da_rodada.upper()}")
        if len(self.lista_palavras) == 0:
            print("VOCE ZEROU!!")
            return False
        print("Aperte [ENTER] para continuar.")
        return True

    def ler_txt(self, nome_do_arquivo:str="5.txt") -> list:
        lista_palavras = []
        try:
            with open(nome_do_arquivo, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                for palavra in conteudo.split("\n"):
                    if len(palavra) == self.n_letras:
                        lista_palavras.append(palavra)
        except:
            with open(f'CLI_Termo./{nome_do_arquivo}', 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                for palavra in conteudo.split("\n"):
                    if len(palavra) == self.n_letras:
                        lista_palavras.append(palavra)
        return lista_palavras

    def nao_mais_loop_principal(self, input:str):
        if not self.continuar:
            self.nova_rodada()
            self.continuar = True
        self.exibir_tela()
        entrada_valida = self.entrada_tem_n_letras_certinho(input)
        if entrada_valida:
            terminou = self.nova_tentativa(input)
            self.exibir_tela()
            if terminou:
                self.continuar = False
                self.encerrar()
                return
        return
    
    def inserir_input(self, input:str):
        self.nao_mais_loop_principal(input)


termo:Termo|None = None

def init():
    global termo
    termo = Termo(seed=0, max_tentativas=5, n_letras=5)
    termo.exibir_tela()
    return termo



# py -m http.server