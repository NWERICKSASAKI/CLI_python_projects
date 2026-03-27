
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
            return 'Utilize "pip install nome_do_pacote" para depois importá-la'
        elif 'No module named' in str(e):
            return 'Utilize "pip install nome_do_pacote" para depois importá-la'
        return f"Error: {str(e)}\n"
    finally:
        sys.stdout = old_stdout
    return buffer.getvalue()


def receber_input(string:str):
    pass

# py -m http.server