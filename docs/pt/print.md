
## Visão Geral

O `DoxBoxPrintManager` (`print.py`) é um componente essencial do sistema DoxBox, projetado para lidar de forma contínua com a impressão de imagens imediatamente após serem capturadas. Este script Python integra-se com o CUPS (Common UNIX Printing System) para gerenciar trabalhos de impressão e garante que cada imagem seja impressa com sucesso, fornecendo feedback em tempo real sobre o status do trabalho. Para garantir a confidencialidade e a segurança dos dados, a imagem é imediatamente excluída após ser enviada à impressora.

## Recursos

- **Integração Direta com o CUPS**: Aproveita o servidor CUPS para enviar e gerenciar trabalhos de impressão, garantindo ampla compatibilidade com várias impressoras.
- **Monitoramento de Trabalhos de Impressão em Tempo Real**: Acompanha o status de cada trabalho de impressão em tempo real, fornecendo atualizações sobre a conclusão, erros ou cancelamentos.
- **Tratamento de Erros e Relatórios**: Mecanismos abrangentes de tratamento de erros relatam problemas de volta ao aplicativo, garantindo uma operação suave.
- **Design Modular**: O script é estruturado em funções claras e concisas, facilitando o entendimento, manutenção e extensão.
- **Configurável**: Utiliza um módulo de configuração externo (`config.py`) para ajustes fáceis sem alterar o script principal.
- **Modo de Depuração**: Inclui um modo de depuração para testes e solução de problemas sem enviar trabalhos de impressão reais para a impressora.

## Componentes

- `send_message_to_app(message)`: Envia mensagens de status ou códigos de erro para o aplicativo principal DoxBox `app.py` para registro ou notificação do usuário.
- `check_print_job_status(conn, job_id)`: Monitora o status dos trabalhos de impressão enviados, garantindo que sejam concluídos com sucesso ou tratando erros conforme necessário.
- `print_image(printer_name, image_path)`: Envia um arquivo de imagem para a impressora especificada e inicia o processo de monitoramento.
- `copy_file(source_path, destination_path)`: Gerencia a transferência segura de arquivos de imagem do local de captura para a fila de impressão.
- `move_image()`: Orquestra o processo de preparação das imagens para impressão, incluindo transferência de arquivos e exclusão pós-impressão.

## Como Funciona

1. **Captura de Imagem**: Uma vez que uma imagem é capturada pelo DoxBox, ela é armazenada em um diretório predeterminado.
2. **Preparação do Arquivo**: A função `move_image` verifica o diretório em busca de novas imagens, preparando-as para impressão.
3. **Impressão**: As imagens são enviadas para a função `print_image`, onde são submetidas como trabalhos de impressão para a impressora configurada.
4. **Monitoramento**: O status de cada trabalho de impressão é monitorado em tempo real por `check_print_job_status`, fornecendo feedback sobre o progresso do trabalho e lidando com quaisquer problemas que surjam.
5. **Conclusão**: Após a impressão bem-sucedida, o arquivo de imagem é excluído e o sistema está pronto para a próxima captura.

## Configuração

O script depende de um arquivo `config.py` separado para configurações, como os detalhes do servidor CUPS, nome da impressora e diretórios para armazenamento e impressão de imagens. Isso permite ajustes fáceis para diferentes ambientes ou impressoras.

## Depuração e Registro

O modo de depuração pode ser ativado para fins de teste, simulando o processo de impressão sem enviar trabalhos para a impressora. O registro no console fornece feedback em tempo real sobre a operação do script.

## Dependências

- CUPS
- Python-CUPS (para interagir com o servidor CUPS do Python)
- Bibliotecas padrão do Python: `datetime`, `shutil`, `socket`, `os`, `time`

## Exemplo de Uso

Exemplo de uso que demonstra como chamar a função `print_image` com valores fixos para o nome da impressora e o caminho da imagem. Este exemplo serve como um guia básico para integrar a funcionalidade de impressão em fluxos de trabalho de aplicativos mais amplos.

```python
printer_name = "Nome_da_Sua_Impressora_Aqui"
image_directory = "/caminho/para/diretorio/de/imagens"
image_file = "exemplo.jpg"

image_path = os.path.join(image_directory, image_file)
print_image(printer_name, image_path)
```

## Introdução

1. Certifique-se de que o CUPS está instalado e configurado no seu sistema.
2. Instale o Python-CUPS usando pip: `pip install pycups`.
3. Ajuste o arquivo `config.py` para corresponder ao seu ambiente.
4. Execute o script após uma imagem ser capturada para iniciar o processo de impressão.

### Instalando Dependências Necessárias no Raspberry Pi:

Para usar o pycups no seu Raspberry Pi, você precisa garantir que as dependências necessárias estejam instaladas. Aqui estão os passos para isso:

1. **Atualize Seu Sistema**: Certifique-se de que suas listas de pacotes e pacotes instalados estejam atualizados.

   ```bash
   sudo apt-get update
   sudo apt-get upgrade
   ```

Isso garantirá que seu Raspberry Pi esteja executando o software mais recente.

**Instale o CUPS e Ferramentas de Desenvolvimento**: Instale o CUPS (Common UNIX Printing System), as bibliotecas de desenvolvimento do CUPS e os cabeçalhos de desenvolvimento do Python. Essas bibliotecas são essenciais para compilar o pycups.

    sudo apt-get install libcups2-dev libcupsimage2-dev gcc python3-dev

Este comando instala as bibliotecas e ferramentas de desenvolvimento necessárias.

**Instale o pycups Usando pip**: Após instalar os pacotes de desenvolvimento necessários, tente instalar o pycups novamente usando pip3.

    pip3 install pycups

A essa altura, você deve conseguir compilar e instalar o pycups com sucesso.

**Atualize pip, setuptools e wheel (Se Necessário)**: Em alguns casos, você pode precisar garantir que seus pacotes pip, setuptools e wheel estejam atualizados.

    pip3 install --upgrade pip setuptools wheel

Após atualizar esses pacotes, tente instalar o pycups novamente.
