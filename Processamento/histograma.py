import cv2
import numpy as np

# Calcula o histograma da imagem em tons de cinza
def calcular_histograma(imagem_cinza):
    histograma = cv2.calcHist([imagem_cinza], [0], None, [256], [0, 256])
    return histograma

