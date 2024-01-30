# Documentação para main.py

## Visão Geral

O script `main.py` serve como ponto de entrada central para a aplicação, orquestrando vários componentes e gerenciando sua execução com base em modos operacionais. Ele utiliza encadeamento (threading) e subprocessos para executar diferentes partes da aplicação em paralelo, proporcionando flexibilidade na depuração e teste de funcionalidade.

## Dependências

- **Bibliotecas Padrão**: threading, subprocess
- **Módulos do Projeto**: config, app.py, switch.py (condicionalmente `./dev/process_mock.py` e `./dev/debug_client.py` para depuração)

## Configuração

O script utiliza configurações do módulo `config`, em particular a flag `DEBUG_MODE`, para determinar o modo operacional (debug ou padrão).

## Recursos

- **Execução Concorrente**: Utiliza encadeamentos (threads) para executar `app.py` e potencialmente um processo de simulação em paralelo.
- **Depuração Condicional**: Dependendo do `DEBUG_MODE`, pode executar processos de depuração adicionais para auxiliar no desenvolvimento e teste.
- **Gerenciamento de Subprocessos**: Executa componentes-chave (`app.py`, `switch.py` ou processos de depuração) como subprocessos, garantindo ambientes de execução isolados e controlados.

## Funções

### `run_app()`

Executa `app.py` como um subprocesso. Este script contém a funcionalidade central da aplicação e é sempre executado, independentemente do modo de depuração.

### `run_app2()`

Executa um processo de simulação (`./dev/process_mock.py`) como um subprocesso, destinado a ser usado no modo de depuração para fins de desenvolvimento ou teste.

### `run_switch_or_debug_as_subprocess()`

Determina se deve executar `switch.py` ou o cliente de depuração (`./dev/debug_client.py`) com base na flag `DEBUG` da configuração. No modo padrão, é executado `switch.py`, que pode ser responsável pelo controle de hardware, switches de rede ou outras funções essenciais da aplicação. No modo de depuração, o cliente de depuração é executado para facilitar a depuração e o desenvolvimento.

## Fluxo de Execução

1. **Inicialização**: O script começa lançando `app.py` em um encadeamento (thread) separado para garantir que sua funcionalidade principal seja executada em paralelo com outros componentes.
2. **Verificação do Modo de Depuração**: Se a aplicação estiver no modo de depuração, ele inicia adicionalmente um processo de simulação em outro encadeamento para desenvolvimento ou teste.
3. **Execução de Componentes**: Dependendo do modo operacional, `main.py` executa ou `switch.py` para operações padrão ou um cliente de depuração para fins de depuração.

## Executando o Script

Para executar a aplicação, execute o seguinte comando no terminal:

```bash
python main.py
