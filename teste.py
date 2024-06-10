# Importando bibliotecas necessárias
import os  # Biblioteca para interagir com o sistema operacional
import tkinter as tk  # Biblioteca para criar interfaces gráficas
from tkinter import filedialog, messagebox  # Módulos do tkinter para diálogos de arquivos e mensagens
import tkinter.ttk as ttk  # Módulo do tkinter para widgets adicionais
import yt_dlp  # Biblioteca para download de vídeos do YouTube
import ffmpeg  # Biblioteca para manipulação de áudio e vídeo
import pickle  # Biblioteca para serialização de objetos Python
from threading import Thread  # Biblioteca para criar threads (execuções paralelas)

class AplicativoBaixadorYouTube:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Baixador de YouTube")  # Definindo o título da janela
        self.raiz.geometry("400x200")  # Definindo o tamanho da janela

        self.pasta_destino = tk.StringVar()  # Variável para armazenar o caminho da pasta de destino
        self.texto_status = tk.StringVar()  # Variável para armazenar o texto de status
        self.texto_status.set("")

        self.carregar_configuracoes()  # Carrega as configurações salvas

        # Criando e posicionando widgets na janela
        etiqueta_link = tk.Label(self.raiz, text="Link do YouTube:")
        etiqueta_link.pack()

        self.entrada_link = tk.Entry(self.raiz, width=50)
        self.entrada_link.pack()

        quadro_pasta = tk.Frame(self.raiz)
        quadro_pasta.pack()

        etiqueta_pasta = tk.Label(quadro_pasta, text="Pasta de Destino:")
        etiqueta_pasta.pack(side=tk.LEFT)

        self.entrada_pasta = tk.Entry(quadro_pasta, textvariable=self.pasta_destino, width=40)
        self.entrada_pasta.pack(side=tk.LEFT)

        botao_pesquisar = tk.Button(quadro_pasta, text="Pesquisar", command=self.pesquisar_pasta)
        botao_pesquisar.pack(side=tk.LEFT)

        self.barra_progresso = ttk.Progressbar(self.raiz, orient="horizontal", length=380, mode="determinate")
        self.barra_progresso.pack(pady=5)

        etiqueta_status = tk.Label(self.raiz, textvariable=self.texto_status)
        etiqueta_status.pack()

        botao_baixar = tk.Button(self.raiz, text="Baixar", command=self.iniciar_download)
        botao_baixar.pack(pady=5)

    def pesquisar_pasta(self):
        # Abre um diálogo para selecionar a pasta de destino
        pasta_selecionada = filedialog.askdirectory()
        if pasta_selecionada:
            self.pasta_destino.set(pasta_selecionada)

    def iniciar_download(self):
        # Inicia o processo de download
        link = self.entrada_link.get()
        pasta_destino = self.pasta_destino.get()
        if not link or not pasta_destino:
            messagebox.showerror("Erro", "Por favor insira um link do YouTube e um diretório.")
            return

        self.salvar_configuracoes()

        self.barra_progresso["value"] = 0
        self.texto_status.set("Baixando...")

        # Inicia o download em uma nova thread
        thread_download = Thread(target=self.baixar_video, args=(link, pasta_destino))
        thread_download.start()

    def baixar_video(self, link, pasta_destino):
        # Função para baixar o vídeo do YouTube
        try:
            opcoes_ydl = {
                'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),  # Define o modelo do nome do arquivo
                'format': 'bestaudio/wav',  # Define o formato do arquivo baixado
            }
            with yt_dlp.YoutubeDL(opcoes_ydl) as ydl:
                ydl.download([link])
            self.barra_progresso["value"] = 100
            self.texto_status.set("Download completo!")
        except Exception as e:
            self.texto_status.set("Erro: " + str(e))

    def salvar_configuracoes(self):
        # Salva as configurações no arquivo settings.pkl
        configuracoes = {'pasta_destino': self.pasta_destino.get()}
        with open('configuracoes.pkl', 'wb') as f:
            pickle.dump(configuracoes, f)

    def carregar_configuracoes(self):
        # Carrega as configurações do arquivo settings.pkl
        try:
            with open('configuracoes.pkl', 'rb') as f:
                configuracoes = pickle.load(f)
                self.pasta_destino.set(configuracoes['pasta_destino'])
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicativoBaixadorYouTube(raiz)
    raiz.mainloop()
