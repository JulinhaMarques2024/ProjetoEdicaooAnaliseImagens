import cv2
import numpy as np

# Aplica o alargamento de contraste para expandir os valores de intensidade
def realce_contraste(img_cinza):
    val_min = np.min(img_cinza)
    val_max = np.max(img_cinza)
    imagem_expandida = (img_cinza - val_min) * (255 / (val_max - val_min))
    return imagem_expandida.astype(np.uint8)

# Aplica equalização de histograma para melhorar o contraste
def histograma_equalizado(img_cinza):
    return cv2.equalizeHist(img_cinza)

