# Documentação para switch.py

## Visão Geral

O módulo `switch.py` é um componente crítico da aplicação, responsável por monitorar dados de API externa, detectar mudanças significativas e comunicar-se com outras partes da aplicação para acionar ações específicas com base nessas mudanças. Ele usa requisições de rede, threading e programação de soquete para atingir seus objetivos.

## Dependências

- **Bibliotecas Padrão**: requests, time, threading, socket
- **Módulos do Projeto**: config

## Configuração

O módulo depende de várias configurações definidas no módulo `config`, incluindo:

- `API_URL`: A URL da API externa a ser monitorada.
- `API_KEY`: A chave necessária para autenticação na API.
- `HOST, PORT`: Configurações de rede para comunicação por soquete.
- `AMOUNT_THRESHOLD`: Um valor de limite específico que aciona uma ação quando atingido.
- `CHECK_INTERVAL`, `POST_PAYMENT_DELAY`: Intervalos de tempo para ritmo operacional.

## Funções Chave

### `send_message_to_app(message)`

Envia uma mensagem para outro componente da aplicação (possivelmente `app.py`) usando programação de soquete. Esta função encapsula a lógica de comunicação em rede, incluindo o tratamento de erros.

### `main_loop()`

A função principal que é executada em um loop contínuo, realizando as seguintes ações:

1. Obtém dados de uma API externa usando a biblioteca `requests`.
2. Monitora mudanças nos dados, especificamente procurando por alterações em um valor de `payment_hash`.
3. Quando uma mudança é detectada e certas condições são atendidas (por exemplo, um limite de valor), aciona uma ação enviando uma mensagem para outro componente.
4. Incorpora mecanismos de atraso para gerenciar a frequência de solicitações de API e ações subsequentes.

## Fluxo de Execução

1. Inicializa e inicia o loop principal em uma thread separada para garantir uma execução não bloqueante.
2. Monitora continuamente uma API externa em busca de mudanças, usando um valor de hash como indicador.
3. Comunica-se com outros componentes da aplicação via soquetes para coordenar ações com base em mudanças detectadas.

## Executando o Módulo

Para executar o `switch.py`, execute o seguinte comando em um terminal:

```bash
python switch.py
