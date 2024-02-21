
## Visão Geral
Este módulo serve como ponto de entrada para o DoxBox, orquestrando a inicialização e a gestão de vários componentes, incluindo um servidor de aplicação, servidor LED e utilidades adicionais para depuração e controle de dispositivos.

## Dependências
- Python 3
- Módulo `subprocess` para execução de scripts.
- Módulo `threading` para execução concorrente.
- `pigpiod` para controle de LED (instalado e executado separadamente).
- **Módulos do Projeto**: `led.py`, `app.py`, `switch.py` (condicionalmente `./dev/process_mock.py` e `./dev/debug_client.py` para depuração)

## Componentes Chave

### 1. Servidor de Aplicação
- **Funcionalidade**: Gerencia a lógica principal da aplicação.
- **Script**: `app.py`

### 2. Servidor LED
- **Funcionalidade**: Controla operações de LED.
- **Script**: `led.py`
- **Dependências**: Requer o daemon `pigpiod` para controle dos pinos GPIO.

### 3. Ferramentas de Depuração
- **Funcionalidade**: Fornece capacidades de depuração.
- **Scripts**: `debug_client.py` e `process_mock.py`
- **Modos**: Controlado pela variável `DEBUG` em `config.py`.

### 4. Controle de Dispositivos
- **Funcionalidade**: Gerencia operações específicas do dispositivo como pagamento e impressão.
- **Script**: `switch.py`

## Configuração
As configurações, incluindo o modo de depuração, são gerenciadas através de `config.py`. Ajuste as configurações neste arquivo para controlar o comportamento da aplicação.

## Executando a Aplicação
1. Inicie a aplicação executando `main.py`.
2. O script inicializa o servidor de aplicação e o servidor LED em threads separadas.
3. Dependendo do modo de depuração definido em `config.py`, ele inicia as ferramentas de depuração ou o script de controle de dispositivos.

## Modo de Depuração
- **Nível 0**: Operação normal, `switch.py` é executado.
- **Nível 1**: Depuração básica, `debug_client.py` é executado.
- **Nível 2**: Depuração estendida, tanto `debug_client.py` quanto `process_mock.py` são executados.

## Estendendo a Aplicação
Para adicionar novas funcionalidades:
1. Crie um novo script para o componente.
2. Defina uma função em `main.py` para executar o script, similar a `run_app()` ou `start_led()`.
3. Adicione uma chamada de thread ou subprocesso em `main()` para executar a nova função.

## Solução de Problemas
- Certifique-se de que `pigpiod` esteja instalado e possa ser iniciado pelo script.
- Verifique se todos os scripts referenciados (`app.py`, `led.py`, `switch.py`, etc.) estão presentes nos diretórios esperados.
- Verifique `config.py` para as configurações corretas do modo de depuração.

## Recursos

1. **Execução Concorrente**: Utiliza threads para executar `app.py` e potencialmente um processo simulado em paralelo.
2. **Depuração Condicional**: Dependendo do `DEBUG_MODE`, pode executar processos de depuração adicionais para auxiliar no desenvolvimento e testes.
3. **Gestão de Subprocessos**: Executa componentes chave (`app.py`, `switch.py` ou processos de depuração) como subprocessos, garantindo ambientes de execução isolados e controlados.

## Executando o Script

Para executar a aplicação, execute o seguinte comando no terminal:

```bash
python3 main.py
```
