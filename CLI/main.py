
import io
import sys

contexto = {}

def executar_codigo(codigo):
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    try:
        try:
            resultado = eval(codigo, contexto)
            if resultado is not None:
                print(resultado)
        except:
            exec(codigo, contexto)
    except Exception as e:
        if 'is included in the Pyodide' in str(e):
            return '<div class="custom_output">Utilize "pip install nome_do_pacote" para depois importá-la</div>'
        elif 'No module named' in str(e):
            return '<div class="custom_output">Utilize "pip install nome_do_pacote" para depois importá-la</div>'
        return f'<div class="custom_output">Error: {str(e)}</div>'
    finally:
        sys.stdout = old_stdout
    saida:str = buffer.getvalue()
    saida = saida.replace('<', '&lt;').replace('>', '&gt;')
    return f'<div class="output" style="white-space: pre-wrap;">{saida}</div>'


def receber_input(string:str):
    pass

# py -m http.server