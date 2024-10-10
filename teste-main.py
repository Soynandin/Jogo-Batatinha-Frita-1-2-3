import tkinter as tk
import random
from PIL import Image, ImageTk

# Variáveis do jogo
boneca_olhos_abertos = False
movimento_detectado = False
distancia_inicial = None
faixa_de_erro = 10  # Faixa de erro aceitável para a movimentação

# Função para simular a captura da distância
def capturar_distancia():
    return random.randint(50, 100)  # Simulação da captura de distância (em cm)

# Função para iniciar o jogo
def iniciar_jogo():
    global boneca_olhos_abertos, distancia_inicial, movimento_detectado
    movimento_detectado = False
    boneca_olhos_abertos = False
    distancia_inicial = None

    botao_iniciar.place_forget()

    # Exibe "Quer me desafiar?" com fundo branco e texto preto
    label_contagem.config(text="Quer me desafiar?", fg="black", bg="white", font=("Arial", 48))
    label_contagem.place(relx=0.5, rely=0.5, anchor="center")  # Centralizado na tela
    janela.after(2000, iniciar_contagem)

# Função para exibir a contagem regressiva
def iniciar_contagem():
    # Exibe "Prepare-se" e a contagem de 3 segundos
    label_contagem.config(text="Prepare-se", fg="black", bg="white", font=("Arial", 48))
    janela.after(1000, lambda: label_contagem.config(text="1", font=("Arial", 72)))
    janela.after(2000, lambda: label_contagem.config(text="2"))
    janela.after(3000, lambda: label_contagem.config(text="3"))
    janela.after(4000, comecar_jogo)

# Função para iniciar o jogo após a contagem
def comecar_jogo():
    global boneca_olhos_abertos
    boneca_olhos_abertos = False
    label_contagem.config(text="Não há ninguém olhando...", fg="white", bg="black", font=("Arial", 48))

    # Coloca a mensagem no topo e atualiza o fundo para preto, sem imagens
    label_contagem.place(relx=0.5, rely=0.1, anchor="center")
    atualizar_imagem_boneca(None)

    tempo_contagem = random.uniform(1, 3)
    janela.after(int(tempo_contagem * 1000), verificar_movimento)

# Função para verificar o movimento
def verificar_movimento():
    global boneca_olhos_abertos, distancia_inicial
    
    boneca_olhos_abertos = True
    label_contagem.config(text="Vigiando!", fg="white", bg="black", font=("Arial", 48))

    # Coloca a mensagem "Vigiando!" na parte superior
    label_contagem.place(relx=0.5, rely=0.1, anchor="center")

    # Exibe os olhos vigiando sobre o fundo preto
    atualizar_imagem_boneca(olhos_vigiando_exibido)
    
    # Captura a distância inicial quando a boneca começa a vigiar
    distancia_inicial = capturar_distancia()
    
    if distancia_inicial is not None:
        janela.after(5000, verificar_resultado)  # Espera 5 segundos para verificar o movimento

# Função para verificar o resultado após o movimento
def verificar_resultado():
    global boneca_olhos_abertos, distancia_inicial
    
    distancia_atual = capturar_distancia()

    if distancia_atual is not None:
        # Se a diferença de distância exceder a faixa de erro, o jogador perde
        if abs(distancia_atual - distancia_inicial) > faixa_de_erro:
            label_contagem.config(text="Você perdeu!!", fg="white", bg="black", font=("Arial", 72))
            label_contagem.place(relx=0.5, rely=0.1, anchor="center")  # Manter a mensagem no topo
            mostrar_botao_reload()
        else:
            label_contagem.config(text="Você sobreviveu nessa, tem sorte...", fg="white", bg="black", font=("Arial", 48))
            label_contagem.place(relx=0.5, rely=0.1, anchor="center")  # Manter a mensagem no topo
            janela.after(2000, comecar_jogo)

# Função para mostrar o botão de reiniciar
def mostrar_botao_reload():
    botao_reload.place(relx=0.5, rely=0.9, anchor="center")

# Função para reiniciar o jogo
def reiniciar_jogo():
    botao_reload.place_forget()

    # Reseta a tela para branco com fundo e imagem dos olhos desaparecendo
    canvas.config(bg="white")
    atualizar_imagem_boneca(None)

    # Exibe "Quer me desafiar?" com fundo branco
    label_contagem.config(text="Quer me desafiar?", fg="black", bg="white", font=("Arial", 48))
    label_contagem.place(relx=0.5, rely=0.5, anchor="center")  # Coloca a mensagem no centro

    janela.after(2000, iniciar_contagem)

# Função para atualizar a imagem da boneca
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