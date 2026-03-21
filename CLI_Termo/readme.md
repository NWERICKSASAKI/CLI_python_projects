# TERMO no CLI do Python

Originalmente, para praticar orientado a objetos, e também por tédio, resolvi fazer eu mesmo um termo em Python para ficar bricando no terminal.  

O tempo passou e passei a desenvolver um jogo mais complexo para ser jogado pelo terminal, porém, não é nada versátil enviar um arquivo para meus amigos executarem em seus computadores para poder jogar...  

...foi aí que pensei, será que consigo subir como página estática no github pages?  

Pesquisei e descobri que através de HTML, javascript posso integrar com o pyodide e resolvi aceitar o desafio de adaptar meus mini-games de terminal para ser jogados no navegador, simulando o CLI.  

Sei que o projeto aqui é bem básico, mas aprendi bastante coisa!

## O código original

Fiz o Termo em um arquivo .py para rodar diretamento no terminal, se quiser consultá-lo, está ali no arquivo [_termo.py](_termo.py)  

Como estava precisando praticar um pouco mais de POO resolvi quebrar a lógica do jogo e cada letra exibida em classes.  

Afinal, cada letra guardava o valor que o jogador chutou, tem a letra correspondente da palavra secrete e sua respectiva cor.

O jogo rodava em loop, sempre aguardando input do usuário e inserindo prints constantes para cada interação do jogador.

Para quem quiser brincar de termo, com mais "vidas" ou até mesmo com um dicionário de palavras personalizadas ou com tamanho de palavras diferentes, fique a vontade para clonar o projeto e explorar!

## A adaptação

Dará pra perceber que boa parte do código foi reaproveitado mas parte da lógica e fluxo dos processos foram alterados no [main.py](main.py):

* primeiro o `print()` original eu sobrescrevi para poder gerar tags HTML para ser exibido no navegador;
* segundo, o `Colorama` que dava cores ao terminal teve que ser substituído por adaptações de tags HTML com classes para ter cores via CSS;
* terceiro, a lógica original, como em qualquer *game engine* parte de um loop, tive que desfazer para adaptar o jogo rodar a partir de cada interação via "input" do HTML/JS.

O resultado você pode visualizar na página estática ->
