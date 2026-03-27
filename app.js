let pyodide;
const input = document.getElementById("input")
const output = document.getElementById("output")

async function init() {
    pyodide = await loadPyodide()

    // p inserir o arquivo local ao diretorio (local) do python
    const texto = await fetch("projetos.json").then(r => r.text());
    pyodide.FS.writeFile("projetos.json", texto);

    const code = await fetch("main.py").then(r => r.text())
    await pyodide.runPythonAsync(code);
    await pyodide.runPython(`le_json_diretorios()`)
    await get_output_and_update_front();
    input.removeAttribute("disabled");
    input.focus();
}

async function enviar(){
    const entrada_usuario = input.value;
    pyodide.globals.set("entrada_usuario", entrada_usuario)
    const resultado = pyodide.runPython(`recebe_input(entrada_usuario)`);
    await get_output_and_update_front()
    if (!resultado == '') go_to_page(resultado);
    
}

async function get_output_and_update_front(){
    response = await pyodide.runPython(`output`);
    output.innerHTML = response;
}

function go_to_page(folder){
    window.location.href = window.location.href + folder;
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