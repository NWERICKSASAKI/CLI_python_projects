# CLI do Python no Navegador

🎮 Sempre fui fã de tentar fazer meu próprios jogos, e as vezes no meu tempo livre praticando python faço uns programinhas para rodar no CLI (e tambpem mini-games)

🤔 ...mas as vezes pros meus coleguinhas mais leigos fica meio ruim deles testarem meus programinhas, seja instalando bibliotecas, ou tentar rodar um `compilado.exe` e o anti-vírus (ou eles) ficarem com receio de ser malicioso.

💡 Pesquisei e descobri que através de HTML, javascript posso integrar com o **pyodide** e rodar tudo no GitHub Pages e resolvi aceitar o desafio de adaptar meus mini-games e programas de terminal para ser acessados no navegador, simulando o CLI.  

## Como funciona

⚙️ Tudo funciona numa página estática HTML + JS + CSS, usando o pyodide ele interpreta o meu código python e roda as funções isoladamentes a cada `ENTER` que dou no programa e interpreta o `input` e retorna o resultado do python (adaptado em uma string com elementos HTML para renderizar).  

😓 Porém eu fui estudando um pouco mais do **pyodide** e seus potenciais eu acabei divergindo do meu objetivo original de só rodar meus programas e acabei criando este simulador de CLI em Python → [CLI_PlayTest](/CLI_PlayTest)

## Adaptando para meus outros programas

⚠️ Descobri que o **pyodide** possui algumas limitações, por exemplo, não vamos ter mais os nossos `print()` e `input()`, além de outros vários outros detalhes.

E o que isso afeta?  
Boa parte das lógicas dos meus programas **:(**  

🔁 Afinal, não vou poder mais fazer um loop até receber um `input()` que válido (e avisar com `print()` que o usuário digitou uma opção inválida)

Então boa parte das lógicas que eu usava teriam que ser reformuladas para não mais rodar no famoso `if __name__ == '__main__`, e sim por chamada via função do meu HTML/JS a cada `ENTER` que dou no input.

Se quiser ver o resultado, sinta-se a vontade de navegar nas pastas deste repositório e visitar suas respectivas páginas estáticas!  

## Testando localmente

Para testar localmente, será necessário rodar no terminal:  

`py -m http.server`

Depois abrir o navegador em:

`http://localhost:8000/`

## Projetos futuros

Por enquanto vou adaptando os códigos que gostaria de compartilhar, fazendo algumas melhorias visuais.  
🎯 Mas vamos destacar o que gostaria de fazer:

- [x] Já que comecei um CLI, vou melhorando aos poucos, tipo resgatar comandos anteriores apertando `↑`.
- [ ] Similar ao CLI, queria fazer um playtest em python para digitar um código de +5 linhas e rodar e ver o resultado
- [ ] (tentar) Fazer algo similar ao Jupyther notebook.
- [x] Trazer meu mini-game de cartas chamado scouldrel que eu vi no youtube e recriei em python.
