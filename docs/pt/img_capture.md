# Documentação para img_capture.py

## Visão Geral

O script `img_capture.py` é um componente integral da aplicação projetada para gerenciar fluxos de trabalho de captura de imagens. Ele se comunica com câmeras digitais por meio do utilitário de linha de comando gphoto2, realizando tarefas como captura de imagens, download para um diretório designado e gerenciamento de convenções de nomeação de arquivos. Além disso, incorpora comunicação de rede para enviar atualizações de status ou erros para outras partes da aplicação.

## Dependências

- **Utilitários Externos**: Requer o gphoto2 instalado no sistema (`sudo apt-get install gphoto2`).
- **Bibliotecas Padrão**: `socket`, `datetime`, `os`, `subprocess`, `signal`
- **Módulos do Projeto**: `config`

## Funcionalidades Principais

### Interação com a Câmera

- Utiliza comandos gphoto2 para interagir diretamente com a câmera, permitindo operações como acionar a captura de imagens, fazer o download de imagens e limpar o cartão de memória da câmera.

### Gerenciamento de Processos

- Inclui funcionalidade para encerrar processos específicos do sistema que possam interferir no acesso à câmera, garantindo controle exclusivo sobre a câmera durante a operação.

### Gerenciamento de Arquivos e Diretórios

- Manipula a criação de diretórios de saída para armazenar imagens capturadas, com tratamento de erros comuns, como diretórios existentes ou erros de permissão.
- Implementa lógica de renomeação de arquivos para organizar e gerenciar imagens capturadas com base em convenções de nomeação predefinidas.

### Comunicação de Rede

- Apresenta uma função para enviar mensagens a outros componentes da aplicação por meio de sockets TCP, facilitando a comunicação entre processos e relatórios de status.

## Funções Principais

### `send_message_to_app(message)`

Envia mensagens de status ou códigos de erro para outro componente da aplicação, aprimorando a manipulação de erros e os mecanismos de feedback do usuário.

### `kill_process()`

Procura e encerra um processo específico por nome, geralmente usado para garantir que a câmera não esteja sendo acessada por outro processo.

### `create_output_folder()`

Cria um diretório para armazenar imagens capturadas, tratando graciosamente erros comuns do sistema de arquivos.

### `run_gphoto2_command(command)`

Executa um comando gphoto2 especificado para interação com a câmera, envolto em lógica de tratamento de erros para capturar e comunicar quaisquer problemas encontrados durante a execução.

### `rename_pics()`

Renomeia imagens capturadas com base em um conjunto de critérios, como data e hora, para facilitar a organização e o gerenciamento de arquivos.

## Uso

O script foi projetado para ser executado como parte de um fluxo de trabalho de aplicação maior, normalmente invocado quando a funcionalidade de captura de imagem é necessária. Ele opera em uma sequência de etapas que preparam o sistema e a câmera, executam a captura de imagens e gerenciam os arquivos resultantes.

### Exemplo de Fluxo de Trabalho

1. Encerramento de Processos: Certifique-se de que nenhum processo conflitante esteja acessando a câmera.
2. Preparação de Diretório: Crie ou valide a existência do diretório de saída para armazenar imagens.
3. Captura de Imagem: Acione a captura de imagens e lide com a interação da câmera.
4. Gerenciamento de Arquivos: Faça o download das imagens para o diretório de saída e renomeie-as de acordo com os requisitos da aplicação. Excluir todos os arquivos da câmera.

## Considerações

- Certifique-se de que o gphoto2 esteja instalado e configurado corretamente no sistema onde a aplicação está sendo executada.
- O script deve ter permissões apropriadas para interagir com a câmera, o sistema de arquivos e os sockets de rede.
- Garanta que nenhum outro processo gphoto2 esteja bloqueando a câmera. Para matar o processo, use os comandos:
```bash
ps -A | grep gphoto
```
- Mate processos como gvfs-gphoto2-vo, etc.
## Instalação do gphoto2

Para habilitar a funcionalidade de controle de câmera DSLR do projeto, você precisa instalar o gphoto2 em seu Raspberry Pi ou qualquer sistema baseado no Debian. O gphoto2 é um utilitário versátil de linha de comando que facilita a interação com uma ampla variedade de câmeras digitais.

**Veja como instalar o gphoto2**:

1. **Atualize o seu Sistema**: Primeiro, certifique-se de que suas listas de pacotes e pacotes instalados estejam atualizados.

   ```sh
   sudo apt-get update

2. **Instale o gphoto2**: Use o seguinte comando para instalar o pacote gphoto2 e suas dependências.
    ```sh
    sudo apt-get install gphoto2

Este comando irá baixar e instalar automaticamente o gphoto2, tornando-o disponível em seu sistema.

Com o gphoto2 instalado com sucesso, seu Raspberry Pi ou sistema baseado no Debian será capaz de se comunicar e controlar câmeras DSLR para funcionalidades de captura de imagens.

Para obter informações mais detalhadas sobre o gphoto2 e suas extensas capacidades, [você pode visitar o site oficial do gPhoto.](http://www.gphoto.org/doc/remote/)