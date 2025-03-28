# Simple Keylogger

Este é um projeto educacional que demonstra como criar um keylogger simples em Python. **Este projeto é apenas para fins educacionais e de aprendizado. Não use este código para atividades maliciosas ou ilegais.**

## Estrutura do Projeto

- `dependencies.bat`: Script para instalar as dependências necessárias (funciona apenas no Windows).
- `keylogger.py`: O script que deve ser executado na máquina da vítima para capturar as teclas pressionadas.
- `server.py`: O servidor Flask que recebe e exibe os logs de teclas capturados.
- `readme.md`: Este arquivo, com informações sobre o projeto.

## Como Funciona

1. O arquivo `keylogger.py` captura as teclas pressionadas na máquina da vítima e envia os dados para o servidor.
2. O arquivo `server.py` é executado na máquina do atacante (hacker) e exibe os logs de teclas e a janela ativa em tempo real.

## Avisos

- **Uso Ético**: Este projeto é apenas para aprendizado. Usar este código para invadir a privacidade de outras pessoas ou para qualquer atividade ilegal é estritamente proibido.
- **Responsabilidade**: O autor não se responsabiliza por qualquer uso indevido deste código.

## Requisitos

- Python 3.7 ou superior.
- Sistema operacional Windows para o script `dependencies.bat`.

## Instalação

### Para o Hacker (Servidor)

1. Certifique-se de ter o Python instalado.
2. Instale as dependências necessárias:
   ```bash
   pip install flask