let pyodide;
const input = document.getElementById("input")
const output = document.getElementById("output")
const palavras_reservadas = {
    'cls':limpar_terminal
}
const inputs=['']
let input_index = -1;

async function init() {
    pyodide = await loadPyodide()
    await pyodide.loadPackage("micropip");
    await pyodide.runPythonAsync('import micropip')

    // await pyodide.loadPackage("pandas");
    const code = await fetch("main.py").then(r => r.text())
    await pyodide.runPythonAsync(code);
    input.removeAttribute("disabled");
    input.focus();
    output.innerHTML=''
}

function limpar_terminal(){
    document.getElementById("output").innerHTML = ''
}

async function enviar(){

    const codigo = input.value;
    inputs.push(codigo)
    output.innerHTML+=`<div class="input">${codigo}</div>`

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
        output.innerHTML += resultado
    }
}

async function instalar_pacote(pacote) {
    success = false;
    error_log = '';
    output.innerHTML += `<div class="custom_output">Instalando pacote ${pacote}...</div>`

    try {
        await pyodide.loadPackage(pacote);
        output.innerHTML += `<div class="custom_output">Pacote ${pacote} instalado com sucesso!</div>`
        success = true;
        return;
    } catch (error) {
        error_log += `<div class="custom_output">Erro ao carregar o pacote ${pacote} com loadPackage: ${error}</div>`
    }

    if (!success){
        try {
            await pyodide.runPythonAsync(`await micropip.install("${pacote}")`);
            output.innerHTML += `<div class="custom_output">Pacote ${pacote} instalado com sucesso!</div>`
            success = true;
            return;
        } catch (error) {
            error_log += `<div class="custom_output">Erro ao instalar o pacote ${pacote} com micropip: ${error}</div>`
        }
    }

    output.innerHTML += error_log;
}

init();

document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        enviar();
        input.value = ""
    } else if (event.key === "ArrowUp") {
        if (inputs.length > 0){
            input_index = (input_index + 1) % inputs.length;
            input.value = inputs[input_index];
        }
    } else if (event.key === "ArrowDown") {
        if (inputs.length > 0){
            input_index = (input_index - 1) % inputs.length;
            if (input_index < 0){
                input_index = inputs.length - 1;
            }
            input.value = inputs[input_index];
        }
    }

    input.focus();
});

// py -m http.server