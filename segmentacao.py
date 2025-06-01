import cv2
import numpy as np

# Aplica a segmentação automática usando o método de Otsu
def aplicar_otsu(img_cinza):
    _, limiarizada = cv2.threshold(img_cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return limiarizada