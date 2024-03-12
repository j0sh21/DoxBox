# DoxBox - uma cabine fotográfica com bitcoin ⚡️ lightning

<p align="center">
<img src="https://raw.githubusercontent.com/j0sh21/DoxBox/main/docs/images/Box.jpeg" width="200">
</p>



## Componentes Principais


- **main.py**: Atua como ponto de entrada da aplicação, orquestrando a execução de vários componentes com base nos modos operacionais.
- **app.py**: Gerencia a interface gráfica do usuário (GUI) da aplicação, facilitando interações do usuário e exibindo informações.
- **switch.py**: Lida com interações de API externas e executa ações específicas com base nos dados recebidos, como acionar outros componentes da aplicação.
- **img_capture.py**: Interage com câmeras para capturar imagens, baixá-las e gerenciar o armazenamento de arquivos, utilizando gphoto2.
- **print.py (Em Progresso)**: Interface com impressoras usando CUPS para imprimir imagens, com funcionalidade para selecionar impressoras e gerenciar trabalhos de impressão.
- **config.py**: Contém configurações usadas em toda a aplicação, como chaves de API, nomes de dispositivos e caminhos de arquivos.


## Requisitos de Hardware

- **Raspberry Pi 4** executando o sistema operacional baseado em Debian [disponível na página oficial de software do Raspberry Pi](https://www.raspberrypi.com/software/operating-systems/).
- **Câmera DSLR**: Canon EOS 450D com pelo menos 1GB de cartão SD. Se usar outra, [verifique a compatibilidade com o gphoto2 no site oficial](http://www.gphoto.org/proj/libgphoto2/support.php).
- **Display**: Waveshare 10.4" QLED Quantum Dot Display Capacitivo (1600 x 720).
- **Impressora**: Xiaomi-Instant-Photo-Printer-1S, suporta o sistema de impressão CUPS, papel fotográfico de 6".
- **LED**: Tira de LED RGB de 4 canais, junto com uma placa de ensaio, cabos de conexão e 4 Mosfets para controle.
- **Material de Construção**: Três chapas de madeira compensada de 80x80cm; o acesso a um cortador a laser pode ser benéfico.
- **Hardware de Montagem**: 20 conjuntos de ímãs de canto (2 peças por conjunto), 40 parafusos de 4mm de diâmetro e 120 porcas de 4mm de diâmetro para fixar os componentes.
- **Cor de spray**: 1 lata de primer, 4 latas da cor real.


  <img src="https://github.com/j0sh21/DoxBox/assets/63317640/384280e0-cc6e-4bd0-9953-c318b5e12f15" height="200">
  <img src="https://github.com/j0sh21/DoxBox/assets/63317640/e446af16-d840-4cbc-87f9-3d5f67b3a15d" height="200">
  <img src="docs/images/poc.gif" height="200">

## Exemplo de fluxo de programa:
<img src="docs/images/flowchart.JPG" height="1100">

## Instruções de Configuração

1. **Clone o Repositório**: Comece clonando este repositório para sua máquina local.

```sh
git clone https://github.com/j0sh21/DoxBox.git
```

2. **Instale as Dependências**: Certifique-se de que o Python está instalado no seu sistema e, em seguida, instale os pacotes Python necessários.



```sh
pip install -r requirements.txt
```

**Nota**: Alguns componentes podem exigir dependências adicionais a nível de sistema (por exemplo, gphoto2, CUPS).

- Se quiser instalar dependências adicionais a nível de sistema automaticamente, execute install.sh em vez disso:

```sh
cd DoxBox/install
chmod u+x install.sh
./install.sh
```

3. **Configure**: Revise e atualize config/cfg.ini com suas configurações específicas, como nomes de dispositivos, chaves de API e caminhos de arquivos.



```sh
nano cfg.ini
```

## Uso

Para executar a aplicação, navegue até o diretório do projeto e execute `main.py`:

```sh
python3 main.py
 ````
Para funcionalidades específicas, como capturar uma imagem ou imprimir, você pode executar os scripts respectivos (por exemplo, python3 img_capture.py para captura de imagem).
Exemplo de Uso

**Capturar uma Imagem** Certifique-se de que sua câmera esteja conectada e reconhecida pelo seu sistema, e depois execute:

 ```sh
python3 img_capture.py
 ```
**Imprimir uma Imagem**: Atualize o print.py com o nome da sua impressora e o caminho do arquivo de imagem e execute:
 ```sh
python3 print.py
 ```
## Contribuições
Contribuições para o projeto são bem-vindas! Consulte as diretrizes de contribuição para obter mais informações sobre como enviar solicitações de pull, relatar problemas ou sugerir melhorias.

# Registro de Alterações para o Projeto FotoBox
## Versão 0.1 lançado 25 de Fev 2024

### Funcionalidades
- Atualizado `app.py` para usar novos quadros e novos GIFs.
- Integrados novos GIFs de @arbadacarbaYK, removendo quadros de fundo vazios e marcas d'água. GIFs de contagem regressiva agora têm tempos consistentes entre os números.
- Adicionado `self.isreplay` para resetar a contagem de loops do GIF apenas uma vez.
- Introduzidos novos códigos de erro de `switch.py` na documentação em Português, Inglês e Alemão.
- Implementado novo estado 3.5: Transição para `img_capture.py` após o primeiro GIF de sorriso terminar.
- Implementado novo estado 3.9: Foto transferida com sucesso da câmera, iniciando a preparação para impressão.
- Antecipado o estado 4: Acionado mais cedo para começar a impressão antes da foto ser deletada da câmera.
- Refatorado o tratamento de erros específicos da câmera em `img_capture.py`.
- Introduzidas tentativas máximas de repetição e tempos de espera variáveis para erros relacionados à câmera.

### Melhorias
- Verificação de conectividade de rede antes de consultar a API LNbits.
- Melhorado e limpo o estilo da saída do console.
- Cursor do mouse ocultado para uma interface mais limpa.
- Mensagens de log aprimoradas em clareza e detalhe.
- Arquivos corrompidos removidos e limpeza geral realizada.
- Efeitos de LED ajustados para um feedback visual melhor.

### Correções
- Corrigido `def kill_process()` para garantir o término adequado do processo.
- Corrigido o problema onde vários GIFs de sorriso poderiam ser exibidos simultaneamente.
- Resolvido um bug onde o estado 204 poderia permanecer indefinidamente em falhas na verificação de trabalhos de impressão.

### Infraestrutura
- Criada uma pasta de saída para trabalhos de impressão. **TODO:** Automatizar a criação de pastas usando `os.mkdir` em vez de incluir uma pasta vazia no repositório.
- **TODO:** Ajustar a funcionalidade de `check_print_job_status`.

## Contribuindo

Contribuições para o projeto são bem-vindas! Por favor, consulte as diretrizes de contribuição para informações sobre como enviar pull requests, relatar problemas ou sugerir melhorias.

## Licença
Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter detalhes.
## Agradecimentos
Agradecimentos especiais a todos os contribuidores e mantenedores das bibliotecas e ferramentas externas usadas neste projeto.

