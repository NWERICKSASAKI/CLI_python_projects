let pyodide;

const input = document.getElementById("input")
const output = document.getElementById("output")

async function init() {
    pyodide = await loadPyodide()
    const code = await fetch("main.py").then(r => r.text())
    await pyodide.runPythonAsync(code);
}


async function enviar(){
    const codigo = input.value;
    pyodide.globals.set("entrada_usuario", entrada_usuario)
    output.innerText = pyodide.runPython(`receber_input(entrada_usuario)`);
}

init();

document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
    enviar();
    input.value = ""
    }
});

// py -m http.server