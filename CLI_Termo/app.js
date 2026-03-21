let pyodide;

const input = document.getElementById("input")
const output = document.getElementById("output")

async function init() {
    pyodide = await loadPyodide()

    await pyodide.loadPackage("micropip");

    // p instalar bibliotecas
    // ala `pip install Unidecode`
    await pyodide.runPythonAsync(`
    import micropip
    await micropip.install("Unidecode")
    `);

    // p inserir o arquivo local ao diretorio (local) do python
    const texto = await fetch("5.txt").then(r => r.text());
    pyodide.FS.writeFile("5.txt", texto);

    const code = await fetch("main.py").then(r => r.text())
    await pyodide.runPythonAsync(code);

    response = await pyodide.runPython(`init()`);
    await to_output(response);
}

async function enviar(){
    const entrada_usuario = input.value;
    pyodide.globals.set("entrada_usuario", entrada_usuario);
    response = await pyodide.runPython(`receber_input(entrada_usuario)`);
    await to_output(response);
    console.log(response)
}

async function to_output(str){
    output.innerHTML = str
}

init();

document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
    enviar();
    input.value = ""
    }
});

// py -m http.server