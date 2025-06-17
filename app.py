from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
import os
import secrets
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Importações dos módulos
from Processamento.filtros import *
from Processamento.segmentacao import aplicar_otsu
from Processamento.morfologia import aplicar_erosao, aplicar_dilatacao
from Processamento.transformacoes import realce_contraste, histograma_equalizado
from Processamento.histograma import calcular_histograma

# Configuração do app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Pastas
UPLOAD_FOLDER = 'static/uploads'
PROCESSING_FOLDER = 'static/processing'
HISTOGRAMA_PATH = 'static/histograma.png'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSING_FOLDER'] = PROCESSING_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSING_FOLDER, exist_ok=True)

# ---------------------- ROTAS ----------------------

@app.route('/')
def index():
    return redirect(url_for('upload_page'))

@app.route('/upload_page')
def upload_page():
    return render_template('upload.html')

@app.route('/carregar_imagem', methods=['POST'])
def carregar_imagem():
    imagem = request.files.get('imagem')
    if not imagem or imagem.filename == '':
        return redirect(url_for('upload_page'))

    filename = secure_filename(imagem.filename)
    caminho = os.path.join(UPLOAD_FOLDER, filename)
    imagem.save(caminho)

    # Carrega e redimensiona
    img = cv2.imread(caminho)
    altura, largura = img.shape[:2]
    nova_largura = 800
    if largura > nova_largura:
        nova_altura = int((nova_largura / largura) * altura)
        img = cv2.resize(img, (nova_largura, nova_altura), interpolation=cv2.INTER_AREA)

    # Converte para tons de cinza e salva
    img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(caminho, img_cinza)

    # Limpa processamento anterior
    session['imagem_nome'] = filename
    session.pop('imagem_processada', None)

    return redirect(url_for('processar'))

@app.route('/processar')
def processar():
    imagem_nome = session.get('imagem_nome')
    imagem_processada = session.get('imagem_processada')
    if not imagem_nome:
        return redirect(url_for('upload_page'))
    return render_template('processar.html',
                           imagem_nome=imagem_nome,
                           imagem_processada=imagem_processada)

@app.route('/aplicar_filtro', methods=['POST'])
def aplicar_filtro():
    filtro = request.form.get('filtro')
    base = request.form.get('base')
    filename = session.get('imagem_nome')

    if not filename or not filtro:
        return redirect(url_for('processar'))

    if base == 'processada' and session.get('imagem_processada'):
        path = os.path.join(PROCESSING_FOLDER, filename)
    else:
        path = os.path.join(UPLOAD_FOLDER, filename)

    img_cinza = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img_cinza is None:
        return 'Imagem não encontrada', 400

    # Aplicar filtros (todos agora recebem imagem em escala de cinza)
    if filtro == 'media':
        resultado = media_filtro(img_cinza)
    elif filtro == 'mediana':
        resultado = mediana_filtro(img_cinza)
    elif filtro == 'gaussiano':
        resultado = gauss_filtro(img_cinza)
    elif filtro == 'maximo':
        resultado = max_filtro(img_cinza)
    elif filtro == 'minimo':
        resultado = min_filtro(img_cinza)
    elif filtro == 'laplaciano':
        resultado = laplaciano_filtro(img_cinza)
    elif filtro == 'roberts':
        resultado = roberts_filtro(img_cinza)
    elif filtro == 'prewitt':
        resultado = prewitt_filtro(img_cinza)
    elif filtro == 'sobel':
        resultado = sobel_filtro(img_cinza)
    elif filtro == 'frequencia_pbaixa':
        resultado = filtrar_frequencia(img_cinza, modo='passa-baixa')
    elif filtro == 'frequencia_palta':
        resultado = filtrar_frequencia(img_cinza, modo='passa-alta')
    elif filtro == 'otsu':
        resultado = aplicar_otsu(img_cinza)
    elif filtro == 'erosao':
        resultado = aplicar_erosao(img_cinza)
    elif filtro == 'dilatacao':
        resultado = aplicar_dilatacao(img_cinza)
    elif filtro == 'realce':
        resultado = realce_contraste(img_cinza)
    elif filtro == 'equalizacao':
        resultado = histograma_equalizado(img_cinza)
    else:
        return 'Filtro inválido', 400

    # Salva imagem processada
    saida = os.path.join(PROCESSING_FOLDER, filename)
    cv2.imwrite(saida, resultado)
    session['imagem_processada'] = filename

    return redirect(url_for('processar'))

@app.route('/histograma')
def histograma():
    filename = session.get('imagem_processada') or session.get('imagem_nome')
    if not filename:
        return redirect(url_for('upload_page'))

    caminho = os.path.join(PROCESSING_FOLDER if session.get('imagem_processada') else UPLOAD_FOLDER, filename)
    img = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)

    hist = calcular_histograma(img)
    plt.figure(figsize=(8, 4))
    plt.plot(hist, color='black')
    plt.title('Histograma')
    plt.xlabel('Intensidade')
    plt.ylabel('Frequência')
    plt.tight_layout()
    plt.savefig(HISTOGRAMA_PATH)
    plt.close()

    return render_template('histograma.html', imagem_histograma='histograma.png')

# Servir arquivos
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/processing/<filename>')
def processed_file(filename):
    return send_from_directory(PROCESSING_FOLDER, filename)

@app.route('/download/<filename>')
def download_imagem_processada(filename):
    return send_from_directory(PROCESSING_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

