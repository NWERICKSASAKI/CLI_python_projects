let pyodide;
const input = document.getElementById("input")
const output = document.getElementById("output")

async function init() {
    pyodide = await loadPyodide()
    const code = await fetch("main.py").then(r => r.text())
    await pyodide.runPythonAsync(code);
    await get_output_and_update_front();
    input.removeAttribute("disabled");
    input.focus();
}

async function enviar(){
    const entrada_usuario = input.value;
    pyodide.globals.set("entrada_usuario", entrada_usuario)
    const resultado = pyodide.runPython(`recebe_input(entrada_usuario)`);
    if (resultado > 0) go_to_page(resultado);
    await get_output_and_update_front()
    
}

async function get_output_and_update_front(){
    response = await pyodide.runPython(`output`);
    output.innerHTML = response;
}

function go_to_page(index){

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