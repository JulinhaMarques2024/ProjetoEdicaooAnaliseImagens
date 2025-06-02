from flask import Flask, render_template, request
import cv2
import numpy as np
from Processamento.filtros import (
    media_filtro,
    mediana_filtro,
    gauss_filtro,
    max_filtro,
    min_filtro,
    laplaciano_filtro,
    roberts_filtro,
    prewitt_filtro,
    sobel_filtro,
    filtrar_frequencia,
)
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'imagem' not in request.files:
        return 'Nenhum arquivo enviado', 400

    file = request.files['imagem']
    if file.filename == '':
        return 'Nenhum arquivo selecionado', 400

    filtro = request.form.get('filtro')

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Carrega a imagem
    img = cv2.imread(filepath)
    img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplica o filtro selecionado
    if filtro == 'media':
        img_editada = media_filtro(img)
    elif filtro == 'mediana':
        img_editada = mediana_filtro(img)
    elif filtro == 'gaussiano':
        img_editada = gauss_filtro(img)
    elif filtro == 'maximo':
        img_editada = max_filtro(img)
    elif filtro == 'minimo':
        img_editada = min_filtro(img)
    elif filtro == 'laplaciano':
        img_editada = laplaciano_filtro(img_cinza)
    elif filtro == 'roberts':
        img_editada = roberts_filtro(img_cinza)
    elif filtro == 'prewitt':
        img_editada = prewitt_filtro(img_cinza)
    elif filtro == 'sobel':
        img_editada = sobel_filtro(img_cinza)
    elif filtro == 'frequencia_baixa':
        img_editada = filtrar_frequencia(img_cinza, modo='passa-baixa')
    elif filtro == 'frequencia_alta':
        img_editada = filtrar_frequencia(img_cinza, modo='passa-alta')
    else:
        return filtro , 400

    # Salva a imagem resultante
    resultado_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resultado.png')
    cv2.imwrite(resultado_path, img_editada)

    return render_template('resultado.html', imagem_original=filename, imagem_editada='resultado.png', filtro = filtro)



from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)


