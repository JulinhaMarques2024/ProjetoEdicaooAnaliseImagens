import cv2
import numpy as np

# =========================
# FILTROS PASSA-BAIXA
# =========================

# Aplica o filtro da média (suaviza a imagem)
def media_filtro(img):
    return cv2.blur(img, (5, 5))

# Aplica o filtro da mediana (reduz ruído preservando bordas)
def mediana_filtro(img):
    return cv2.medianBlur(img, 5)

# Aplica o filtro gaussiano (suavização com peso maior ao centro)
def gauss_filtro(img):
    return cv2.GaussianBlur(img, (5, 5), 0)

# Aplica o filtro máximo (dilatação) para destacar regiões brilhantes
def max_filtro(img):
    estrutura = np.ones((5, 5), np.uint8)
    return cv2.dilate(img, estrutura)

# Aplica o filtro mínimo (erosão) para destacar regiões escuras
def min_filtro(img):
    estrutura = np.ones((5, 5), np.uint8)
    return cv2.erode(img, estrutura)

# =========================
# FILTROS PASSA-ALTA
# =========================

# Aplica o filtro Laplaciano para detecção de bordas
def laplaciano_filtro(img_cinza):
    return cv2.Laplacian(img_cinza, cv2.CV_64F)

# Aplica o filtro de Roberts para detecção de bordas diagonais
def roberts_filtro(img_cinza):
    kernel_x = np.array([[1, 0], [0, -1]])
    kernel_y = np.array([[0, 1], [-1, 0]])
    grad_x = cv2.filter2D(img_cinza, -1, kernel_x)
    grad_y = cv2.filter2D(img_cinza, -1, kernel_y)
    return cv2.magnitude(grad_x.astype(float), grad_y.astype(float))

# Aplica o filtro de Prewitt para detecção de bordas horizontais e verticais
def prewitt_filtro(img_cinza):
    kernel_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    grad_x = cv2.filter2D(img_cinza, -1, kernel_x)
    grad_y = cv2.filter2D(img_cinza, -1, kernel_y)
    return cv2.magnitude(grad_x.astype(float), grad_y.astype(float))

# Aplica o filtro de Sobel para detecção de bordas suaves
def sobel_filtro(img_cinza):
    grad_x = cv2.Sobel(img_cinza, cv2.CV_64F, 1, 0, ksize=5)
    grad_y = cv2.Sobel(img_cinza, cv2.CV_64F, 0, 1, ksize=5)
    return cv2.magnitude(grad_x, grad_y)

# =========================
# CONVOLUÇÃO NO DOMÍNIO DA FREQUÊNCIA
# =========================

# Aplica um filtro no domínio da frequência (passa-baixa ou passa-alta)
def filtrar_frequencia(img_cinza, modo='passa-baixa'):
    dft = cv2.dft(np.float32(img_cinza), flags=cv2.DFT_COMPLEX_OUTPUT)
    deslocado = np.fft.fftshift(dft)
    linhas, colunas = img_cinza.shape
    centro_linha, centro_coluna = linhas // 2, colunas // 2

    mascara = np.zeros((linhas, colunas, 2), np.uint8)
    raio = 30
    if modo == 'passa-baixa':
        mascara[centro_linha - raio:centro_linha + raio, centro_coluna - raio:centro_coluna + raio] = 1
    else:
        mascara[:, :] = 1
        mascara[centro_linha - raio:centro_linha + raio, centro_coluna - raio:centro_coluna + raio] = 0

    filtrada = deslocado * mascara
    inversa = np.fft.ifftshift(filtrada)
    imagem_reconstruida = cv2.idft(inversa)
    imagem_final = cv2.magnitude(imagem_reconstruida[:, :, 0], imagem_reconstruida[:, :, 1])
    return cv2.normalize(imagem_final, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)