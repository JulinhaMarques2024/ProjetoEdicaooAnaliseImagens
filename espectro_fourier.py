import cv2
import numpy as np

# Calcula e retorna o espectro de magnitude da Transformada de Fourier
def gerar_espectro(img_cinza):
    dft = cv2.dft(np.float32(img_cinza), flags=cv2.DFT_COMPLEX_OUTPUT)
    deslocado = np.fft.fftshift(dft)
    magnitude = 20 * np.log(cv2.magnitude(deslocado[:, :, 0], deslocado[:, :, 1]) + 1)
    return cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)




