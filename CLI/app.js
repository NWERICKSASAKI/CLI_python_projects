let pyodide;
const input = document.getElementById("input")
const output = document.getElementById("output")
const palavras_reservadas = {
    'cls':limpar_terminal
}

async function init() {
    pyodide = await loadPyodide()
    await pyodide.loadPackage("micropip");
    await pyodide.runPythonAsync('import micropip')

    // await pyodide.loadPackage("pandas");
    const code = await fetch("main.py").then(r => r.text())
    await pyodide.runPythonAsync(code);
    input.removeAttribute("disabled");
    input.focus();
    output.innerText=''
}

function limpar_terminal(){
    document.getElementById("output").innerText = ''
}

async function enviar(){

    const codigo = input.value;
    let texto_output = codigo + '\n' 

    // Comandos fixos
    if (codigo in palavras_reservadas){
        palavras_reservadas[codigo]()
        return
    }

    // Comandos dinâmicos
    const match = codigo.match(/^pip install (.+)$/);

    if (match){
        const pacote = match[1];
        await instalar_pacote(pacote);
        return;
    }

    // Comandos Python
    pyodide.globals.set("codigo", codigo)

    const resultado = pyodide.runPython(`executar_codigo(codigo)`);
    if (resultado.length > 0){
        texto_output += resultado
    }
    output.innerText += texto_output;
}

async function instalar_pacote(pacote) {
    success = false;
    error_log = '';
    output.innerText += `Instalando pacote ${pacote}...\n`

    try {
        await pyodide.loadPackage(pacote);
        output.innerText += `Pacote ${pacote} instalado com sucesso!\n`
        success = true;
        return;
    } catch (error) {
        error_log += `Erro ao carregar o pacote ${pacote} com loadPackage: ${error}\n`
    }

    if (!success){
        try {
            await pyodide.runPythonAsync(`await micropip.install("${pacote}")`);
            output.innerText += `Pacote ${pacote} instalado com sucesso!\n`
            success = true;
            return;
        } catch (error) {
            error_log += `Erro ao instalar o pacote ${pacote} com micropip: ${error}\n`
        }
    }

    output.innerText += error_log;
}

init();

document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        enviar();
        input.value = ""
    }
    input.focus();
});

// py -m http.server