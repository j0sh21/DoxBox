# Documentação para app.py

## Visão Geral
`app.py` serve como um módulo crucial na aplicação, orquestrando a interface do usuário e facilitando as interações do usuário. Este módulo utiliza o poderoso framework PyQt5 para construir uma interface gráfica do usuário (GUI) robusta e responsiva, tornando-o uma peça central para aplicações que requerem interação do usuário através de uma interface visual.

## Propósito

O propósito principal do `app.py` é definir a estrutura e o comportamento da GUI da aplicação. Ele encapsula o design e a funcionalidade de vários componentes da UI, incluindo janelas, widgets, layouts e manipuladores de eventos, garantindo uma experiência de usuário contínua e intuitiva.

## Escopo

Dentro do `app.py`, você encontrará definições para classes e funções chave que, coletivamente, constroem a frente da aplicação. Isso inclui:

- **AppState**: Uma classe projetada para gerenciar o estado da aplicação, permitindo atualizações dinâmicas e interações dentro da GUI. Ela usa um sinal `stateChanged` para notificar outras partes da aplicação quando o estado muda, promovendo um design reativo onde a UI pode se ajustar com base no estado atual da aplicação.
- **VendingMachineDisplay**: Uma subclasse de `QWidget` personalizada que atua como o principal recipiente para os elementos da UI da aplicação, organizando-os em um layout coerente e funcional.

## Manipulação de Estado

A classe `AppState` é central para a gestão de estado da aplicação. Ela mantém uma variável `state` que reflete a condição ou modo atual da aplicação. Mudanças neste estado são propagadas através do sinal `stateChanged`, permitindo que outros componentes, especialmente a UI, reajam e se atualizem de acordo. Esta abordagem desacopla a gestão de estado da lógica da UI, melhorando a modularidade e a manutenibilidade.

## Programação de Sockets e Comunicação Servidor-Cliente

A aplicação possui um componente de servidor que escuta por conexões de entrada usando a biblioteca `socket` do Python. A função `start_server` inicializa este servidor, que aguarda mensagens dos clientes. Ao receber uma mensagem, a função `handle_client_connection` a processa e atualiza o `AppState`, aproveitando o sistema de gestão de estado para refletir as mudanças na UI dinamicamente. Esta configuração de servidor-cliente permite controle remoto ou automatizado sobre a aplicação, ideal para cenários semelhantes a quiosques ou máquinas de venda automática.

## Principais Características

- **Design Modular**: `app.py` segue uma abordagem modular, separando preocupações entre gerenciamento de estado e apresentação da UI, o que facilita a manutenção e escalabilidade.
- **UI Orientada por Estado**: A UI da aplicação responde dinamicamente a mudanças no estado da aplicação, proporcionando uma experiência de usuário reativa que atualiza em tempo real para refletir o contexto e os dados atuais.
- **Integração com PyQt5**: Ao utilizar o PyQt5, `app.py` aproveita um conjunto abrangente de ferramentas e widgets para criar GUIs de nível profissional, incluindo suporte para componentes multimídia, manipulação de eventos e estilização de widgets personalizados.

## Dependências

- **Qt Widgets**: Herda de `QWidget` e pode usar outros widgets como `QLabel`, `QVBoxLayout`, `QHBoxLayout` de PyQt5.QtWidgets.
- **Qt Multimedia**: Potencialmente usa `QCamera`, `QCameraViewfinder` de PyQt5.QtMultimedia e `QCameraViewfinder` de PyQt5.QtMultimediaWidgets para integração com câmeras.
- **Qt Core**: Utiliza classes como `QPixmap`, `QMovie` de PyQt5.QtGui, e `Qt`, `QSize`, `QRect`, `QPoint` de PyQt5.QtCore para funcionalidades básicas da GUI.

## Manipulação de Multimídia e Animações GIF

A classe `VendingMachineDisplay` incorpora capacidades avançadas de manipulação de multimídia, notavelmente para reproduzir e gerenciar animações GIF. Esta funcionalidade aumenta o apelo visual da aplicação e o envolvimento do usuário, especialmente em quiosques interativos ou interfaces de máquinas de venda automática.

### Reprodução de Animações GIF

A aplicação pode exibir animações GIF como parte de sua UI, fornecendo conteúdo visual dinâmico. Isso é alcançado através da classe `QMovie` do PyQt5, que é usada para carregar e reproduzir arquivos GIF. A classe `VendingMachineDisplay` inclui métodos para iniciar a reprodução de um GIF, calcular sua duração e garantir que ele se encaixe nos elementos da UI designados, oferecendo uma experiência multimídia contínua.

### Métodos Principais

- **send_msg_to_LED(host, port, command)**: Este método permite que a aplicação comunique com dispositivos externos, como uma faixa de LED anexada, através de uma rede. Ele estabelece uma conexão de socket com o host e a porta especificados, e então envia um comando, que poderia ser usado para exibir mensagens ou controlar a faixa de LED.
- **calculateDuration()**: Calcula a duração total de uma animação GIF iterando através de seus quadros. Essas informações podem ser usadas para sincronizar a reprodução do GIF com outros eventos na aplicação, garantindo uma experiência de usuário coerente.
- **handle_client_connection(client_socket, appState)**: Lida com conexões de entrada de clientes. Esta função é uma parte crítica da arquitetura servidor-cliente, lendo mensagens enviadas pelos clientes, atualizando o estado da aplicação com base nessas mensagens e garantindo que a UI reflita essas mudanças.
- **start_server(appState)**: Inicializa e inicia o servidor que escuta por conexões de entrada. Ele se vincula a uma porta especificada e espera que os clientes se conectem, criando uma nova thread para lidar com cada conexão, permitindo assim que a aplicação continue operando suavemente enquanto gerencia as solicitações dos clientes.


## Mensagens Tratadas por app.py

A aplicação usa strings numéricas como mensagens para representar diferentes estados e ações dentro da aplicação. Cada mensagem desencadeia comportamentos específicos, correlacionando-se com várias funcionalidades ou feedback visual através da GUI. Abaixo está uma tabela resumindo as mensagens numéricas e seus efeitos correspondentes dentro da aplicação:

**Mensagens de Estado**:

| Mensagem | Descrição                                                                            |
|----------|--------------------------------------------------------------------------------------|
| "0"      | representa um estado inicial ou de boas-vindas.                                      |
| "1"      | indica um pagamento ou transação concluída.                                          |
| "2"      | Inicia a contagem regressiva, fase de preparação após um pagamento.                  |
| "3"      | significa a conclusão de uma contagem regressiva, movendo-se para a captura da foto. |
| "4"      | Foto capturada com sucesso, início da impressão agora.                               |
| "5"      | Impressão concluída: "Obrigado" ou estado de conclusão, o fim de uma transação.      |
| "144"    | Subpago                                                                              |
| "204"    | Imagem excluída com sucesso após impressão.                                          |


**Mensagens de Erro**:

| Mensagem | Descrição                                            |
|----------|------------------------------------------------------|
| "100"    | Erro Geral em app.py.                                |
| "101"    | Câmera não encontrou foco                            |
| "102"    | Nenhuma câmera encontrada                            |
| "103"    | arquivo não encontrado                               |
| "104"    | permissão negada                                     |
| "110"    | erro geral em print.py                               |
| "112"    | impressora não encontrada                            |
| "113"    | arquivo não encontrado                               |
| "114"    | permissão negada                                     |
| "115"    | erro ao copiar arquivo                               |
| "116"    | Trabalho de impressão interrompido ou cancelado.     |
| "119"    | erro ao criar trabalho de impressão                  |
| "120"    | erro geral em img_capture.py                         |
| "130"    | erro geral em led.py                                 |
| "140"    | Erro inesperado em switch.py                         |
| "141"    | Código de status da resposta da API LNbits não é 200 |
| "142"    | Erro de conexão com a API LNbits                     |
| "143"    | Erro inicial de conexão com a API LNbits             |


Essas mensagens são processadas pela aplicação para atualizar o `AppState` e, por extensão, a UI e quaisquer displays externos conectados à aplicação. As ações específicas tomadas em resposta a cada mensagem podem variar dependendo do contexto atual da aplicação e do fluxo de trabalho pretendido.

## Uso

Desenvolvedores que trabalham com `app.py` podem esperar interagir com abstrações de alto nível para componentes da UI, mecanismos diretos para gerenciamento de estado e padrões de programação orientados a eventos. Este módulo é tipicamente invocado como parte do processo de inicialização da aplicação, inicializando a GUI e vinculando-a à lógica e aos modelos de dados subjacentes.

# Documentação da Classe AppState

## Visão Geral

A classe `AppState`, definida dentro de `app.py`, é um componente fundamental projetado para gerenciar o estado da aplicação e permitir a comunicação entre componentes em uma aplicação GUI baseada em Qt. Ela herda de `QObject` para utilizar o mecanismo de sinal-slot do Qt, tornando-a adequada para aplicações que requerem respostas dinâmicas a mudanças de estado.

## Recursos

- **Gerenciamento de Estado**: Centraliza o gerenciamento do estado da aplicação, fornecendo uma única fonte de verdade para a lógica relacionada ao estado.
- **Emissão de Sinal**: Emprega o mecanismo de sinal do Qt (`pyqtSignal`) para emitir eventos quando o estado da aplicação muda, permitindo que outros componentes reajam a essas mudanças de maneira desacoplada.

## Definição da Classe

### Propriedades

- `state`: Uma propriedade que encapsula o estado atual da aplicação. O acesso a esta propriedade é controlado por meio de um getter e um setter para garantir que as mudanças de estado sejam gerenciadas de forma consistente.

### Sinais

- `stateChanged(str)`: Um sinal emitido sempre que o estado muda, carregando o novo valor do estado como uma string. Esse sinal pode ser conectado a slots ou funções dentro de outros componentes, permitindo que eles respondam a mudanças de estado.

## Uso

A classe `AppState` é tipicamente instanciada uma vez e usada em toda a aplicação para gerenciar e observar o estado da aplicação. Componentes que precisam responder a mudanças de estado podem conectar seus slots ou funções ao sinal `stateChanged`.

### Exemplo

```python
# Instanciação
app_state = AppState()

# Conectar uma função ao sinal stateChanged
def on_state_changed(new_state):
    print(f"O estado da aplicação mudou para: {new_state}")

app_state.stateChanged.connect(on_state_changed)

# Atualizar o estado
app_state.state = "1"  # Isso emitirá o sinal stateChanged e invocará on_state_changed
```

# Documentação da Classe VendingMachineDisplay
## Visão Geral

A classe VendingMachineDisplay, definida dentro de app.py, é um componente crucial da interface gráfica do usuário (GUI) da aplicação. Ela herda de QWidget, tornando-a um recipiente versátil para vários elementos da UI. Esta classe é principalmente responsável por construir e gerenciar o layout, os controles e outros elementos visuais que constituem a interface do usuário da aplicação.
## Dependências

- Qt Widgets: Herda de `QWidget` e pode usar outros widgets como `QLabel`, `QVBoxLayout`, `QHBoxLayout` de PyQt5.QtWidgets.
- Qt Multimedia: Potencialmente usa `QCamera`, `QCameraViewfinder` de PyQt5.QtMultimedia e `QCameraViewfinder` de PyQt5.QtMultimediaWidgets para integração com câmeras.
- Qt Core: Utiliza classes como `QPixmap`, `QMovie` de PyQt5.QtGui, e `Qt`, `QSize`, `QRect`, `QPoint` de PyQt5.QtCore para funcionalidades básicas da GUI.

## Recursos

- **Gerenciamento de Layout**: Gerencia a disposição dos elementos da UI usando layouts (por exemplo, `QVBoxLayout`, `QHBoxLayout`), garantindo uma exibição responsiva e organizada.
- **Integração de Estado**: Integra-se com a classe `AppState` para refletir e potencialmente modificar o estado da aplicação com base em interações do usuário ou outros eventos.
- **Suporte a Multimídia**: Se a funcionalidade da câmera for usada, pode incluir recursos como exibição de feed de câmera ao vivo, utilizando `QCamera` e `QCameraViewfinder`.

## Definição da Classe
### Construtor

- `__init__(self, appState)`: Inicializa uma nova instância da classe `VendingMachineDisplay`, tomando um objeto `AppState` como argumento para facilitar a gestão de estado e interação.

### Métodos Principais

- A classe inclui métodos para inicializar componentes da UI, configurar layouts e conectar sinais a slots para manipulação de eventos (por exemplo, cliques de botão, mudanças de estado).

## Uso

A classe `VendingMachineDisplay` é instanciada como parte do processo de configuração da GUI da aplicação, muitas vezes no script principal ou em um módulo de GUI dedicado. Requer uma instância de `AppState` para permitir atualizações e interações da UI baseadas em estado.

### Exemplo

```python
app = QApplication(sys.argv)
app_state = AppState()
vending_machine_display = VendingMachineDisplay(app_state)
vending_machine_display.show()
sys.exit(app.exec_())
```