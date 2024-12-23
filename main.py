import tkinter as tk
import serial
import random
from PIL import Image, ImageTk

# Variáveis do jogo
boneca_olhos_abertos = False
movimento_detectado = False
distancia_inicial = None
faixa_de_erro = 2  # Faixa de erro aceitável para a movimentação
distancia_minima_permitida = 80  # A partir de 80 cm a pessoa está ativa
distancia_maxima_permitida = 100  # Até 100 cm a pessoa começa
distancia_vitoria_minima = 0  # Distância mínima para vencer (em cm)
distancia_vitoria_maxima = 10  # Distância máxima para vencer (em cm)

# Conexão com Arduino
arduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)

# Função para ler a distância real do sensor
def capturar_distancia():
    try:
        arduino.write(b"get_distance\n")
        distancia = arduino.readline().decode('utf-8').strip()
        if distancia:
            return float(distancia)
        return None
    except serial.SerialException as e:
        print(f"Erro na comunicação com o Arduino: {e}")
        return None
    except Exception as e:
        print(f"Erro geral ao capturar a distância: {e}")
        return None

# Função para o jogo
def iniciar_jogo():
    global boneca_olhos_abertos, distancia_inicial, movimento_detectado
    movimento_detectado = False
    boneca_olhos_abertos = False
    distancia_inicial = None

    botao_iniciar.place_forget()

    # Exibe "Vamos Jogar!" com fundo branco e texto preto
    label_contagem.config(text="Vamos Jogar!", fg="black", bg="white", font=("Arial", 48))
    label_contagem.place(relx=0.5, rely=0.1, anchor="center")  # Topo da tela
    janela.after(2000, iniciar_contagem)

def iniciar_contagem():
    # Exibe a contagem de 3 segundos
    label_contagem.config(text="1", fg="black", bg="white", font=("Arial", 72))
    janela.after(1000, lambda: label_contagem.config(text="2"))
    janela.after(2000, lambda: label_contagem.config(text="3"))
    janela.after(3000, comecar_jogo)

def comecar_jogo():
    global boneca_olhos_abertos
    boneca_olhos_abertos = False
    label_contagem.config(text="", fg="white", bg="black")

    # Atualiza o fundo para preto, sem imagens
    atualizar_imagem_boneca(None)

    tempo_contagem = random.uniform(1, 3)
    janela.after(int(tempo_contagem * 1000), verificar_movimento)

def verificar_movimento():
    global boneca_olhos_abertos, distancia_inicial
    
    boneca_olhos_abertos = True
    label_contagem.config(text="Vigiando!", fg="white", bg="black", font=("Arial", 48))

    # Coloca a mensagem "Vigiando!" na parte superior
    label_contagem.place(relx=0.5, rely=0.1, anchor="center")

    # Exibe os olhos vigiando sobre o fundo preto
    atualizar_imagem_boneca(olhos_vigiando_exibido)

    # Aguarda 3 segundos antes de capturar a distância
    janela.after(3000, capturar_e_verificar_distancia)

def capturar_e_verificar_distancia():
    global distancia_inicial
    
    distancia_inicial = capturar_distancia()

    if distancia_inicial is not None:
        # A pessoa começa entre 80 e 100 cm
        if distancia_inicial >= distancia_minima_permitida and distancia_inicial <= distancia_maxima_permitida:
            janela.after(5000, verificar_resultado)
        else:
            label_contagem.config(text="Você perdeu!!", fg="white", bg="black", font=("Arial", 72))
            label_contagem.place(relx=0.5, rely=0.1, anchor="center")
            mostrar_botao_reload()

def verificar_resultado():
    global boneca_olhos_abertos, distancia_inicial
    
    distancia_atual = capturar_distancia()

    if distancia_atual is not None:
        # Verifica se a pessoa venceu
        if distancia_vitoria_minima <= distancia_atual <= distancia_vitoria_maxima:
            label_contagem.config(text="Você venceu!!", fg="white", bg="black", font=("Arial", 72))
            label_contagem.place(relx=0.5, rely=0.1, anchor="center")
            mostrar_botao_reload()
        # Se a distância atual for menor que a inicial (a pessoa se aproximou demais)
        elif boneca_olhos_abertos and distancia_atual < distancia_inicial - faixa_de_erro:
            label_contagem.config(text="Você perdeu!!", fg="white", bg="black", font=("Arial", 72))
            label_contagem.place(relx=0.5, rely=0.1, anchor="center")
            mostrar_botao_reload()
        else:
            label_contagem.config(text="Você sobreviveu nessa, tem sorte...", fg="white", bg="black", font=("Arial", 48))
            label_contagem.place(relx=0.5, rely=0.1, anchor="center")
            janela.after(2000, retornar_olhos_fechados)

def retornar_olhos_fechados():
    atualizar_imagem_boneca(None)
    label_contagem.config(text="Não há ninguém olhando...", fg="white", bg="black", font=("Arial", 48))

def mostrar_botao_reload():
    botao_reload.place(relx=0.5, rely=0.9, anchor="center")

def reiniciar_jogo():
    botao_reload.place_forget()

    # Reseta a tela para branco com fundo e imagem dos olhos desaparecendo
    canvas.config(bg="white")
    atualizar_imagem_boneca(None)

    # Exibe "Vamos Jogar!" com fundo branco
    label_contagem.config(text="Vamos Jogar!", fg="black", bg="white", font=("Arial", 48))
    label_contagem.place(relx=0.5, rely=0.1, anchor="center")

    janela.after(2000, iniciar_contagem)

def atualizar_imagem_boneca(nova_imagem):
    canvas.delete("all")  # Limpa o canvas
    canvas.config(bg="black")  # Fundo preto durante o jogo
    if nova_imagem:
        canvas.create_image(canvas.winfo_width()//2, canvas.winfo_height()//2, image=nova_imagem, anchor="center")
    canvas.image = nova_imagem

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Batatinha Frita 1, 2, 3")
janela.geometry("800x600")

# Carregar as imagens
olhos_vigiando = Image.open("imagens/olhos-vigiando.png")
imagem_botao_iniciar = Image.open("imagens/botao-start.png")
imagem_botao_reiniciar = Image.open("imagens/botao-reiniciar.png")

olhos_vigiando_exibido = ImageTk.PhotoImage(olhos_vigiando)
botao_iniciar_img = ImageTk.PhotoImage(imagem_botao_iniciar)
botao_reload_img = ImageTk.PhotoImage(imagem_botao_reiniciar)

canvas = tk.Canvas(janela)
canvas.place(relwidth=1, relheight=1)  # O canvas cobre toda a janela

# Label de contagem com fundo branco e texto preto
label_contagem = tk.Label(janela, text="Aguardando...", font=("Arial", 24), fg="black", bg="white")
label_contagem.place(relx=0.5, rely=0.1, anchor="center")  # Coloca a mensagem no topo da tela

# Botão de iniciar com imagem
botao_iniciar = tk.Button(janela, image=botao_iniciar_img, command=iniciar_jogo, borderwidth=0)
botao_iniciar.place(relx=0.5, rely=0.5, anchor="center")  # Centraliza o botão de iniciar

# Botão de reiniciar com imagem
botao_reload = tk.Button(janela, image=botao_reload_img, command=reiniciar_jogo, borderwidth=0)

janela.mainloop()
