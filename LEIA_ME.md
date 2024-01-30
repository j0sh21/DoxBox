"""
# Visão Geral do Projeto

Este projeto foi projetado para aproveitar as capacidades de um Raspberry Pi ou qualquer outro sistema hospedeiro baseado no Debian para interagir com uma câmera DSLR para captura de imagens de alta qualidade, enquanto gerencia e interage com um fluxo de trabalho de aplicativo específico, que inclui captura de imagem, impressão e interação dinâmica com a interface do usuário. O aplicativo é executado em Python e se integra a vários sistemas e bibliotecas externas, como o CUPS para impressão e o gphoto2 para controle da câmera, para fornecer sua funcionalidade.

## Componentes Principais

- **main.py**: Serve como ponto de entrada do aplicativo, orquestrando a execução de vários componentes com base nos modos operacionais.
- **app.py**: Gerencia a interface gráfica do usuário (GUI) do aplicativo, facilitando interações do usuário e exibindo informações.
- **switch.py**: Lida com interações de API externas e realiza ações específicas com base nos dados recebidos, como acionar outros componentes do aplicativo.
- **img_capture.py**: Interage com câmeras para capturar imagens, baixá-las e gerenciar o armazenamento de arquivos, aproveitando o gphoto2.
- **print.py (Em Progresso)**: Interage com impressoras usando o CUPS para imprimir imagens, com funcionalidade para selecionar impressoras e gerenciar trabalhos de impressão.
- **config.py**: Contém configurações usadas em todo o aplicativo, como chaves de API, nomes de dispositivos e caminhos de arquivos.

## Requisitos de Hardware

- **Sistema Hospedeiro**: A plataforma principal para executar o aplicativo (por exemplo, Raspberry Pi, mini PC), fornecendo os recursos de computação necessários e conectividade para periféricos.
- **Câmera DSLR**: Usada para capturar imagens de alta qualidade. Certifique-se de compatibilidade com gphoto2 para integração.
- **Webcam**: Uma webcam deve estar conectada e configurada para funcionalidades de captura de imagem.
- **Tela**: Uma tela é necessária para mostrar a GUI, incluindo pré-visualizações de fotos e animações.
- **Impressora**: Uma impressora de fotos configurada e configurada no Sistema Hospedeiro para imprimir imagens, compatível com o CUPS.

## Instruções de Configuração

1. **Clonar o Repositório**: Comece clonando este repositório em sua máquina local.

   ```sh
   git clone https://github.com/j0sh21/DoxBox.git
    ```
2. **Instalar Dependências**: Certifique-se de que o Python esteja instalado em seu sistema e, em seguida, instale os pacotes Python necessários.

    ```sh

    pip install -r requirements.txt
    ```
    **Observação**: Alguns componentes podem exigir dependências de nível de sistema adicionais (por exemplo, gphoto2, CUPS).
   

   - Se você quiser instalar dependências de nível de sistema adicionais automaticamente, execute o install.sh em vez disso:
      ```sh
      chmod install.sh +x
      ./install.sh

3. **Configurar**: Revise e atualize config/cfg.ini com suas configurações específicas, como nomes de dispositivos, chaves de API e caminhos de arquivo.
   ```sh
   nano cfg.ini
## Uso

Para executar o aplicativo, navegue até o diretório do projeto e execute main.py:

 ```sh
python main.py
 ````
Para funcionalidades específicas, como capturar uma imagem ou imprimir, você pode executar os scripts respectivos (por exemplo, python img_capture.py para captura de imagem).
Exemplo de Uso

**Capturar uma Imagem** Certifique-se de que sua câmera esteja conectada e reconhecida pelo seu sistema, e depois execute:

 ```sh
python img_capture.py
 ```
**Imprimir uma Imagem**: Atualize o print.py com o nome da sua impressora e o caminho do arquivo de imagem e execute:

    python print.py

## Contribuições
Contribuições para o projeto são bem-vindas! Consulte as diretrizes de contribuição para obter mais informações sobre como enviar solicitações de pull, relatar problemas ou sugerir melhorias.
## Licença
Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter detalhes.
## Agradecimentos
Agradecimentos especiais a todos os contribuidores e mantenedores das bibliotecas e ferramentas externas usadas neste projeto.

