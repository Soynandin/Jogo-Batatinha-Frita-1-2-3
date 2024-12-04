# Batatinha Frita 1, 2, 3 - Sistema Interativo com Python e Arduino

## Descrição do Projeto

Este projeto é inspirado no jogo "Batatinha Frita 1, 2, 3", apresentado na série **Round 6 (Squid Game)** da Netflix. Assim como na série, o jogo desafia os jogadores a se moverem apenas quando não estão sendo monitorados e ficarem absolutamente imóveis ao serem observados. A diferença é que aqui você joga contra um sistema automatizado, utilizando sensores e lógica programada.

O objetivo é sobreviver às rodadas, aproximando-se cada vez mais da "boneca" (representada por um sensor de ultrassom). O jogo termina quando você vence ao "tampar os olhos" do sistema ou é eliminado por se mover no momento errado.

---

## Como o Jogo Funciona

1. **Preparação inicial**:
   - O jogador começa a uma distância mínima de **2 metros** do sensor de ultrassom.
   - Quando os "olhos da boneca" estão fechados, o sistema não monitora os movimentos do jogador, permitindo que ele se aproxime.

2. **Olhos Abertos**:
   - Após um tempo aleatório (entre 1 e 3 segundos), a boneca abre os olhos e o sistema começa a monitorar.
   - O sistema registra a distância inicial do jogador e monitora se ele se moveu além de uma **faixa de erro predefinida**.

3. **Eliminação**:
   - Se o jogador se mover enquanto está sendo observado, ultrapassando a margem permitida, o jogo termina com uma mensagem de derrota.

4. **Sobrevivência**:
   - Se o jogador permanecer imóvel durante a observação, ele sobrevive à rodada e pode continuar avançando.

5. **Vitória**:
   - O jogador vence ao alcançar o sensor de ultrassom, chegando a uma distância de **0 a 10 cm**, simbolizando que ele "tapou os olhos" do sistema.

Assim como na série *Round 6*, o jogo testa a paciência, a habilidade de controle e os reflexos do jogador.

---

## Requisitos do Sistema

### Hardware
- **Arduino Uno ou compatível**
- **Sensor de Ultrassom (HC-SR04)**  
- Cabo USB para comunicação Arduino-PC

### Software
- Python 3.8 ou superior
- Bibliotecas:
  - `tkinter`
  - `serial` (pySerial)
  - `Pillow` (para manipulação de imagens)

---

## Instalação e Configuração

### Arduino
1. Conecte o **sensor de ultrassom** ao Arduino:
   - `Trigger` no pino **9**.
   - `Echo` no pino **10**.
2. Carregue o código disponível no arquivo `arduino_code.ino` no Arduino IDE e faça o upload para o dispositivo.

### Python
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/batatinha-frita-123.git
   cd batatinha-frita-123

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt

3. Certifique-se de que o Arduino está conectado à porta correta e ajuste o caminho da porta no código Python

---

## Como Jogar
1. Execute o jogo no terminal:
   ```bash
   python main.py

2. Uma janela será aberta com o botão "Iniciar". Clique nele para começar o jogo.
3. Siga as instruções na tela:
4. Mova-se apenas quando os olhos da boneca estiverem fechados.
5. Fique parado quando os olhos estiverem abertos para sobreviver à rodada.
6. Aproxime-se gradualmente até alcançar a meta final.

---

## Melhorias Futuras
- Adicionar sons e efeitos visuais para tornar o jogo mais imersivo.
- Criar um sistema de pontuação baseado no tempo gasto para vencer.
- Implementar um modo multiplayer local ou online.
