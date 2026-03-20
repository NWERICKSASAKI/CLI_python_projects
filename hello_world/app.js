let pyodide;

async function init() {
    pyodide = await loadPyodide()

    const code = await fetch("main.py").then(r => r.text())
    await pyodide.runPythonAsync(code);
}

async function enviar(){
    const nome = document.getElementById("input").value;
    pyodide.globals.set("nome", nome)

    const resultado = pyodide.runPython(`hello(nome)`);
    document.getElementById("output").innerText = resultado;
}

init();

// py -m http.server