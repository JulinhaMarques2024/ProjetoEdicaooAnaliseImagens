import cv2
import numpy as np

# Aplica a operação de erosão (reduz áreas brancas)
def aplicar_erosao(img):
    estrutura = np.ones((5, 5), np.uint8)
    return cv2.erode(img, estrutura, iterations=1)

# Aplica a operação de dilatação (expande áreas brancas)
def aplicar_dilatacao(img):
    estrutura = np.ones((5, 5), np.uint8)
    return cv2.dilate(img, estrutura, iterations=1)