
# Documentação para led.py

Bem-vindo ao módulo Controlador de LED DoxBox! Este documento foi projetado para ajudá-lo a entender e integrar os efeitos de iluminação LED em sua cabine de fotos DoxBox, aprimorando a experiência do usuário durante o pagamento, a tomada de fotos e outras interações.

## Introdução

A classe `RGBLEDController` neste módulo controla LEDs RGB para criar efeitos visuais envolventes. Seja adicionando ambiente durante o processo de tomada de fotos ou fornecendo dicas visuais durante o pagamento, este módulo oferece uma variedade de animações como respiração, piscar e desvanecimento.

### Pré-requisitos

Antes de começar, certifique-se de ter:

- Um setup Raspberry Pi com LEDs RGB conectados aos pinos GPIO especificados.
- Conhecimento básico de programação Python e configuração de pinos GPIO.

## Componentes Principais

### RGBLEDController

Este é o coração do sistema de controle de LED. Ele gerencia as cores e animações dos LEDs conectados ao seu Raspberry Pi.

#### Inicialização

```python
__init__(self, red_pin, green_pin, blue_pin, steps=config.fade_steps, brightness_steps=config.brightness_steps)
```

Inicializa o controlador com os pinos GPIO conectados aos seus LEDs RGB. `steps` e `brightness_steps` permitem controlar a granularidade das animações.

#### Configurando Animações


- `set_fade_speed(self, speed)`: Ajusta a rapidez com que os LEDs desvanecem entre as cores.
- `set_breath_speed(self, speed)`: Define o ritmo do efeito de respiração, onde os LEDs gradualmente se iluminam e escurecem.
- `set_blink_times(self, on_time, off_time)`: Configura a duração da animação de piscar para os LEDs ligados e desligados.


#### Gerenciando Animações

- `set_loop(self, animation_type)`: Escolhe o tipo de animação (por exemplo, "respirar", "piscar", "desvanecer").
- `activate_loop()`: Inicia o loop de animação selecionado. Atenção: Esta função já é chamada em set_loop()
- `interrupt_current_animation(self)`: Interrompe qualquer animação em andamento, útil para feedback imediato do usuário.

#### Controle Direto de LED

- `set_color(self, r, g, b)`: Define diretamente os LEDs para a cor RGB especificada.
- `update_leds(self)`: Atualiza os LEDs com base nas configurações ou animações atuais.


### ServerThread

Para configurações avançadas, a classe `ServerThread` permite que o Controlador de LED DoxBox receba comandos externos (por exemplo, de `app.py`) para alterar dinamicamente os efeitos de LED.

#### Configurando o Servidor

- `__init__(self, host, port, led_controller)`: Prepara o servidor com detalhes de rede e o vincula ao RGBLEDController.
- `run(self)`: Lança o servidor, tornando o DoxBox responsivo a comandos de controle de LED externos.
- 
## Tratamento de Mensagens


**`led.py` executa ações específicas se um comando for enviado por mensagem:**

|Comando	 | Ação |
|-----------------------------------|-----------------------------------------------------------------------------|
| "color 0 255 0" |	define a cor para azul |
| "brightness 200"	 |define o brilho para 200. Faixa 0 - 255 |
| "fadespeed 0.8"	 |define a velocidade de desvanecimento para 0.8 |
| "fade 1" |	inicia o desvanecimento |
| "blinkspeed 0.5 0.5" |	Define o tempo de ligado e desligado em segundos para o efeito de piscar |
| "blink 1"	 |inicia o piscar vezes ilimitadas |
| "blink 10" |	inicia o piscar 10 vezes  |
| "breathbrightness 0.2 0.8"         | Define a faixa de brilho para o efeito de respiração de 20% a 80% de brilho |
| "breathspeed 0.5" | Definindo a velocidade da respiração para 0.5|
| "fade 0", "breath 0" ou "blink 0"  | interrompe o loop de animação dado                                          |
| "breath 1"                         | inicia a respiração ilimitada                                               |
| "breath 5"                         | inicia a respiração 5 vezes                                                 |
| "interrupt"                        | interrompe o loop de animação atual                                         |

## Exemplo de Integração

Aqui está um exemplo simples para integrar efeitos de LED no seu DoxBox:

```python
from led_controller import RGBLEDController, ServerThread

# Inicialize o controlador de LED com os pinos GPIO
led_controller = RGBLEDController(red_pin=17, green_pin=27, blue_pin=22)

# Opcionalmente, inicie um servidor para comandos externos
server = ServerThread(host='0.0.0.0', port=12345, led_controller=led_controller)
server.run()

# Configure um efeito de respiração para o processo de tirar fotos
led_controller.set_loop('breath')
led_controller.activate_loop()
```

## Dicas para uma Excelente Experiência do Usuário

- Use efeitos de respiração suaves e lentos em momentos de inatividade para criar uma atmosfera acolhedora.
- Piscadas rápidas e brilhantes podem sinalizar o início da sequência de fotos ou um pagamento bem-sucedido.
- Considere temas de cores que combinem com a marca DoxBox ou o tema do evento.

## Solução de Problemas

- LEDs não respondem: Verifique suas conexões GPIO e certifique-se de que seu Raspberry Pi tenha a configuração de pinos correta.
- Animações não mudam: Certifique-se de que `interrupt_current_animation` seja chamado antes de mudar as animações.
