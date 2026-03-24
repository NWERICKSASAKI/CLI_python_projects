let pyodide;

const input = document.getElementById("input")
const output = document.getElementById("output")

async function init() {
    pyodide = await loadPyodide()

    await pyodide.loadPackage("micropip");
        
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
    await get_output_and_update_front();
    input.removeAttribute("disabled");
    input.focus();
}

async function enviar(entrada_usuario){
    pyodide.globals.set("entrada_usuario", entrada_usuario);
    await pyodide.runPython(`termo.inserir_input(entrada_usuario)`);
    await get_output_and_update_front();
}

async function get_output_and_update_front(){
    response = await pyodide.runPython(`output`);
    output.innerHTML = response;
}

init();

document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        enviar(input.value);
        input.value = ""
    }
    input.focus();
});

// py -m http.server