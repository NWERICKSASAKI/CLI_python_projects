import random
from unidecode import unidecode

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

        self.output_str:str = ''

    def print(self, *args, classe:str='', sep:str=' ', end:str='</br>', insert_tag=True) -> None:
        '''
        Pseudo-sobrepor a função original print() para converter todo output original
        por uma saída HTML.
        '''
        if len(args) == 0:
            self.output_str += end
            return

        string = str(args[0])
        if len(args)>1:
            string = sep.join(args)

        if classe:
            classe = f' class={classe}'
        if insert_tag:
            self.output_str += f'<span{classe}>{string}</span>{end}'
        else:
            self.output_str += f'{string}{end}'
        return

    def definir_seed(self, n:int):
        random.seed(n)
        self._seed = n

    def nova_rodada(self):
        numero_aleatorio:int = random.randrange(len(self.lista_palavras))
        self.palavra_da_rodada = self.lista_palavras.pop(numero_aleatorio)
        self.tentativa = 0
        self.exibicao:list[list] = []

    def exibir_tela(self):
        self.output_str = ''
        for palavra in self.exibicao:
            # self.print(palavra, insert_tag=False)
            for letra in palavra:
                self.print(letra, end=' ', insert_tag=False)
            self.print()
        for i in range(self.max_tentativas - self.tentativa):
            self.print('_ '*self.n_letras)
        return self.output_str

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
        self.print(f"\nPalavra secreta: {self.palavra_da_rodada.upper()}")
        if len(self.lista_palavras) == 0:
            self.print("VOCE ZEROU!!")
            return False
        self.print("Aperte [ENTER] para continuar.")
        return True

    def ler_txt(self, nome_do_arquivo:str="5.txt") -> list:
        lista_palavras = []
        with open(nome_do_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            for palavra in conteudo.split("\n"):
                if len(palavra) == self.n_letras:
                    lista_palavras.append(palavra)
        return lista_palavras

    def inserir_input(self, input:str) -> str:
        if not self.continuar:
            self.nova_rodada()
            self.continuar = True
        entrada_valida = self.entrada_tem_n_letras_certinho(input)
        if entrada_valida:
            terminou = self.nova_tentativa(input)
            self.exibir_tela()
            if terminou:
                self.continuar = False
                self.encerrar()
                self.nova_rodada()
            return self.output_str
        return self.exibir_tela()

termo:Termo|None = None

def init():
    global termo
    termo = Termo(seed=0, max_tentativas=5, n_letras=5)
    return termo.exibir_tela()

def receber_input(string:str):
    global termo
    
    if termo == None:
        pass

    return termo.inserir_input(string)



# py -m http.server