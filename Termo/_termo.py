'''
Esse era o arquivo original que usei
para criar este termo para rodar diretamento pelo CLI
'''

from colorama import Fore
from pathlib import Path
from os import system
from unidecode import unidecode
import random

AMARELO = Fore.YELLOW
VERDE =  Fore.LIGHTGREEN_EX
BRANCO = Fore.WHITE 
PATH = Path(__file__).parent

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
            return VERDE
        elif self.letra_chutada in self.palavra_resposta:
            return AMARELO
        else:
            return BRANCO

    def __str__(self):
        if self.letra_chutada == self.letra_resposta_unicode:
            return f"{self.cor}{self.letra_resposta}{BRANCO} "
        return f"{self.cor}{self.letra_chutada}{BRANCO} "




class Termo:
    def __init__(self, seed:int=0, max_tentativas=5, n_letras:int=5):
        self._seed:int = seed
        self.max_tentativas = max_tentativas
        self.n_letras = n_letras
        self.tentativa = 0
        self.lista_palavras:list = self.ler_txt(f"{n_letras}l.txt")
        self.palavra_da_rodada = ""
        self.exibicao = []

    def definir_seed(self, n:int):
        random.seed(n)
        self._seed = n

    def nova_rodada(self):
        numero_aleatorio:int = random.randrange(len(self.lista_palavras))
        self.palavra_da_rodada = self.lista_palavras.pop(numero_aleatorio)
        self.tentativa = 0
        self.exibicao:list = []

    def exibir_tela(self):
        system('cls')
        print("- TERMO -\n")
        for palavra in self.exibicao:
            print(palavra)
        for i in range(self.max_tentativas - self.tentativa):
            print('_ '*self.n_letras)

    def nova_tentativa(self):
        entrada = ""
        while not len(entrada)==self.n_letras:
            self.exibir_tela()
            entrada = input("-> ")
        if self.processar_palavra(entrada):
            return True
        self.tentativa += 1
        if self.tentativa == self.max_tentativas:
            return True
        return False

    def processar_palavra(self, palavra):
        palavra_colorida = ""
        for n, letra in enumerate(palavra):
            obj_letra = Letra(n, self.palavra_da_rodada, letra)
            palavra_colorida += str(obj_letra)
        self.exibicao.append(palavra_colorida)
        if palavra == unidecode(self.palavra_da_rodada):
            return True
        return False
    
    def encerrar(self):
        print(f"\nPalavra secreta: {self.palavra_da_rodada.upper()}")
        if len(self.lista_palavras) == 0:
            print("VOCE ZEROU!!")
            return False
        input("Aperte [ENTER] para continuar.")
        return True

    def ler_txt(self, nome_do_arquivo:str="5l.txt") -> list:
        lista_palavras = []
        with open(PATH / nome_do_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            for palavra in conteudo.split("\n"):
                if len(palavra) == self.n_letras:
                    lista_palavras.append(palavra)
        return lista_palavras

    def main_loop(self):
        continuar = True
        self.nova_rodada()
        while continuar:
            terminou = self.nova_tentativa()
            if terminou:
                self.exibir_tela()
                continuar = self.encerrar()
                self.nova_rodada()


if __name__ == "__main__":
    termo = Termo(0,10,6)
    termo.main_loop()
