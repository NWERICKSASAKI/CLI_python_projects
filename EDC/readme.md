# CLI_PlayTest

🎯 Meu foco era adaptar meus programas e mini-games de terminal em python para rodar pelo navegador...  
😅 Mas acabeidivergindo e criando este **CLI PlayTest** enquanto estava estudando **pyodidde**.  

## O código atual

⚙️ Tudo funciona numa página estática HTML + JS + CSS, usando o pyodide ele interpreta o meu código python e roda as funções isoladamentes a cada `ENTER` que dou no programa e interpreta o `input` e retorna o resultado do python (adaptado em uma string com elementos HTML para renderizar).  

😓 Porém eu fui estudando um pouco mais do **pyodide** e seus potenciais eu acabei divergindo do meu objetivo original de só rodar meus programas e acabei criando este simulador de CLI em Python, sabe aquele famoso:

```py
a=1
b=2
print(a+b)
3
```

Bom funciona **\o/**  

🐼 Até um `import pandas as pd` também vai funcionar!  
mas só se acrescenter no JS o código `await pyodide.loadPackage("pandas");`  

Se quiser ver o resultado, só visitar a página estática:
<https://nwericksasaki.github.io/CLI_python_projects/CLI/>

...depois formulo mais este readme...
