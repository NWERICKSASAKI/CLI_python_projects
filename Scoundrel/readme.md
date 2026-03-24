# CLI_Scoundrel

▶️ Certo dia estava no YouTube quando me surgiu um vídeo de recomendação...

🃏 Era de alguém ensinando um jogo chamado **Scoundrel** que é um jogo *roguelike* com baralho...

👍 Testei eu mesmo, achei desafiador e difícil, gostei bastante!

...e resolvi recriá-lo em python, para jogar pelo terminal!

## O código original

🥷 Originalmente, fiz o jogo para jogar no terminal do python, de forma discreta, sem cores e sem muita coisa que chama a atenção.

Mas depois resolvi enfeitar e enchi de cores via `Colorama` e acrescentei até os emojis dos naipes ♣️♥️♠️♦️.

Se quiser dar uma verificada como era o código original de se jogar pelo terminal → [_scoundrel.py](_scoundrel.py)

## O código atual e adaptação

⚙️ Tudo funciona numa página estática HTML + JS + CSS, usando o **pyodide** e através tudo configurei para simular como estivesse usando o terminal. Só escrever o comando e dar um `ENTER` e o programa roda de forma assíncrona.  

🔧 Para ajustes, óbvio, retirei o `Colorama` e sobrescrevi os `Fore.cor` para retornar tags de `<span class="cor">` para ficar colorido no front.  

🔁 Pra minha sorte, não tive que fazer grandes ajustes no algoritmo porque deixei o loop original bem estruturado recebendo o `input` uma única vez e exibindo o display por `print()` também logo em sequência.  

Foi tão tranquilo a transição que nem tive que fazer um outro arquivo python para testes ou debug!  

Se quiser ver o resultado, só visitar a página estática:
<https://nwericksasaki.github.io/CLI_python_projects/Scoundrel/>
