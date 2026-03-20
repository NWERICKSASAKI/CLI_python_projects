let pyodide;
const input = document.getElementById("input")
const output = document.getElementById("output")
const palavras_reservadas = {
    'cls':limpar_terminal
}


async function init() {
    pyodide = await loadPyodide()
    await pyodide.loadPackage("pandas");
    const code = await fetch("main.py").then(r => r.text())
    await pyodide.runPythonAsync(code);
}

function limpar_terminal(){
    document.getElementById("output").innerText = ''
}

async function enviar(){

    const codigo = input.value;
    let texto_output = codigo + '\n' 


    if (codigo in palavras_reservadas){
        palavras_reservadas[codigo]()
        return
    }

    pyodide.globals.set("codigo", codigo)

    const resultado = pyodide.runPython(`executar_codigo(codigo)`);
    if (resultado.length > 0){
        texto_output += resultado
    }
    output.innerText += texto_output;
}

init();

document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
    enviar();
    input.value = ""
    }
});

// py -m http.server