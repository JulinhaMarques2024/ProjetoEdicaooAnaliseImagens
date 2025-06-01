import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from Processamento.histograma import calcular_histograma 

class AppGUI:
    def __init__(self, janela_principal):
        self.janela = janela_principal
        self.janela.title("Projeto para Edição e Análise de Imagens")
        
        # Inicializa imagens
        self.imagem_original = None
        self.imagem_editada = None

        # Área de exibição
        self.exibicao_imagem = tk.Label(janela_principal)
        self.exibicao_imagem.pack()

        # Botões
        botao_abrir = tk.Button(janela_principal, text="Abrir Imagem", command=self.carregar_imagem)
        botao_abrir.pack()

        botao_histograma = tk.Button(janela_principal, text="Histograma", command=self.exibir_histograma)
        botao_histograma.pack()

        botao_salvar = tk.Button(janela_principal, text="Salvar Imagem", command=self.exportar_imagem)
        botao_salvar.pack()

    def carregar_imagem(self):
        caminho_arquivo = filedialog.askopenfilename()
        if caminho_arquivo:
            self.imagem_original = cv2.imread(caminho_arquivo)
            self.imagem_editada = self.imagem_original.copy()
            self.atualizar_exibicao(self.imagem_original)

    def exportar_imagem(self):
        if self.imagem_editada is not None:
            destino = filedialog.asksaveasfilename(defaultextension=".png")
            if destino:
                cv2.imwrite(destino, self.imagem_editada)
                messagebox.showinfo("Salvar", "Imagem salva com sucesso!")

    def atualizar_exibicao(self, imagem_cv):
        imagem_rgb = cv2.cvtColor(imagem_cv, cv2.COLOR_BGR2RGB)
        imagem_pil = Image.fromarray(imagem_rgb)
        imagem_tk = ImageTk.PhotoImage(imagem_pil)
        self.exibicao_imagem.config(image=imagem_tk)
        self.exibicao_imagem.image = imagem_tk  # evita garbage collection

    def exibir_histograma(self):
        if self.imagem_editada is not None:
            imagem_cinza = cv2.cvtColor(self.imagem_editada, cv2.COLOR_BGR2GRAY)
            histograma = calcular_histograma(imagem_cinza)  
            import matplotlib.pyplot as plt
            plt.plot(histograma)
            plt.show()
