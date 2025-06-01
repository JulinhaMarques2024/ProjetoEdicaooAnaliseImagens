import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Importações dos módulos personalizados
from Processamento.histograma import calcular_histograma
from Processamento.filtros import (
    media_filtro, mediana_filtro, gauss_filtro,
    max_filtro, min_filtro,
    laplaciano_filtro, roberts_filtro, prewitt_filtro, sobel_filtro,
    filtrar_frequencia
)

class AppGUI:
    def __init__(self, janela_principal):
        self.janela = janela_principal
        self.janela.title("Projeto para Edição e Análise de Imagens")
        
        self.imagem_original = None
        self.imagem_editada = None

        # Exibição da imagem
        self.exibicao_imagem = tk.Label(self.janela)
        self.exibicao_imagem.pack(pady=10)

        # --- Frame: Ações Básicas ---
        frame_basico = tk.LabelFrame(self.janela, text="Ações Básicas", padx=10, pady=10)
        frame_basico.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_basico, text="Abrir Imagem", command=self.carregar_imagem).pack(side="left", padx=5)
        tk.Button(frame_basico, text="Histograma", command=self.exibir_histograma).pack(side="left", padx=5)
        tk.Button(frame_basico, text="Salvar Imagem", command=self.exportar_imagem).pack(side="left", padx=5)
        tk.Button(frame_basico, text="Restaurar Original", command=self.restaurar_imagem).pack(side="left", padx=5)

        # --- Frame: Filtros Passa-Baixa ---
        frame_passa_baixa = tk.LabelFrame(self.janela, text="Filtros Passa-Baixa (Espacial)", padx=10, pady=10)
        frame_passa_baixa.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_passa_baixa, text="Média", command=self.aplicar_filtro_media).pack(side="left", padx=5)
        tk.Button(frame_passa_baixa, text="Mediana", command=self.aplicar_filtro_mediana).pack(side="left", padx=5)
        tk.Button(frame_passa_baixa, text="Gaussiano", command=self.aplicar_filtro_gauss).pack(side="left", padx=5)
        tk.Button(frame_passa_baixa, text="Máximo", command=self.aplicar_filtro_max).pack(side="left", padx=5)
        tk.Button(frame_passa_baixa, text="Mínimo", command=self.aplicar_filtro_min).pack(side="left", padx=5)

        # --- Frame: Filtros Passa-Alta ---
        frame_passa_alta = tk.LabelFrame(self.janela, text="Filtros Passa-Alta (Espacial)", padx=10, pady=10)
        frame_passa_alta.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_passa_alta, text="Laplaciano", command=self.aplicar_filtro_laplaciano).pack(side="left", padx=5)
        tk.Button(frame_passa_alta, text="Roberts", command=self.aplicar_filtro_roberts).pack(side="left", padx=5)
        tk.Button(frame_passa_alta, text="Prewitt", command=self.aplicar_filtro_prewitt).pack(side="left", padx=5)
        tk.Button(frame_passa_alta, text="Sobel", command=self.aplicar_filtro_sobel).pack(side="left", padx=5)

        # --- Frame: Filtros no Domínio da Frequência ---
        frame_frequencia = tk.LabelFrame(self.janela, text="Filtros no Domínio da Frequência", padx=10, pady=10)
        frame_frequencia.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_frequencia, text="Passa-Baixa", command=lambda: self.aplicar_filtro_frequencia('passa-baixa')).pack(side="left", padx=5)
        tk.Button(frame_frequencia, text="Passa-Alta", command=lambda: self.aplicar_filtro_frequencia('passa-alta')).pack(side="left", padx=5)

    # --- Funções auxiliares ---
    def atualizar_exibicao(self, imagem_cv):
        imagem_rgb = cv2.cvtColor(imagem_cv, cv2.COLOR_BGR2RGB)
        imagem_pil = Image.fromarray(imagem_rgb)
        imagem_tk = ImageTk.PhotoImage(imagem_pil)
        self.exibicao_imagem.config(image=imagem_tk)
        self.exibicao_imagem.image = imagem_tk

    def carregar_imagem(self):
        caminho_arquivo = filedialog.askopenfilename()
        if caminho_arquivo:
            self.imagem_original = cv2.imread(caminho_arquivo)
            self.imagem_editada = self.imagem_original.copy()
            self.atualizar_exibicao(self.imagem_original)

    def restaurar_imagem(self):
        if self.imagem_original is not None:
            self.imagem_editada = self.imagem_original.copy()
            self.atualizar_exibicao(self.imagem_original)

    def exportar_imagem(self):
        if self.imagem_editada is not None:
            destino = filedialog.asksaveasfilename(defaultextension=".png")
            if destino:
                cv2.imwrite(destino, self.imagem_editada)
                messagebox.showinfo("Salvar", "Imagem salva com sucesso!")

    def exibir_histograma(self):
        if self.imagem_editada is not None:
            imagem_cinza = cv2.cvtColor(self.imagem_editada, cv2.COLOR_BGR2GRAY)
            histograma = calcular_histograma(imagem_cinza)
            plt.figure("Histograma")
            plt.plot(histograma)
            plt.xlabel("Intensidade")
            plt.ylabel("Frequência")
            plt.grid()
            plt.show()

    # --- Filtros Espaciais ---
    def aplicar_filtro_media(self):
        self.imagem_editada = media_filtro(self.imagem_editada)
        self.atualizar_exibicao(self.imagem_editada)

    def aplicar_filtro_mediana(self):
        self.imagem_editada = mediana_filtro(self.imagem_editada)
        self.atualizar_exibicao(self.imagem_editada)

    def aplicar_filtro_gauss(self):
        self.imagem_editada = gauss_filtro(self.imagem_editada)
        self.atualizar_exibicao(self.imagem_editada)

    def aplicar_filtro_max(self):
        self.imagem_editada = max_filtro(self.imagem_editada)
        self.atualizar_exibicao(self.imagem_editada)

    def aplicar_filtro_min(self):
        self.imagem_editada = min_filtro(self.imagem_editada)
        self.atualizar_exibicao(self.imagem_editada)

    def aplicar_filtro_laplaciano(self):
        cinza = cv2.cvtColor(self.imagem_editada, cv2.COLOR_BGR2GRAY)
        resultado = laplaciano_filtro(cinza)
        self.imagem_editada = cv2.cvtColor(np.uint8(np.absolute(resultado)), cv2.COLOR_GRAY2BGR)
        self.atualizar_exibicao(self.imagem_editada)

    def aplicar_filtro_roberts(self):
        cinza = cv2.cvtColor(self.imagem_editada, cv2.COLOR_BGR2GRAY)
        resultado = roberts_filtro(cinza)
        self.imagem_editada = cv2.cvtColor(np.uint8(resultado), cv2.COLOR_GRAY2BGR)
        self.atualizar_exibicao(self.imagem_editada)

    def aplicar_filtro_prewitt(self):
        cinza = cv2.cvtColor(self.imagem_editada, cv2.COLOR_BGR2GRAY)
        resultado = prewitt_filtro(cinza)
        self.imagem_editada = cv2.cvtColor(np.uint8(resultado), cv2.COLOR_GRAY2BGR)
        self.atualizar_exibicao(self.imagem_editada)

    def aplicar_filtro_sobel(self):
        cinza = cv2.cvtColor(self.imagem_editada, cv2.COLOR_BGR2GRAY)
        resultado = sobel_filtro(cinza)
        self.imagem_editada = cv2.cvtColor(np.uint8(resultado), cv2.COLOR_GRAY2BGR)
        self.atualizar_exibicao(self.imagem_editada)

    # --- Filtros de Frequência ---
    def aplicar_filtro_frequencia(self, tipo):
        cinza = cv2.cvtColor(self.imagem_editada, cv2.COLOR_BGR2GRAY)
        resultado = filtrar_frequencia(cinza, tipo)
        self.imagem_editada = cv2.cvtColor(resultado, cv2.COLOR_GRAY2BGR)
        self.atualizar_exibicao(self.imagem_editada)
