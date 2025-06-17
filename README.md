Projeto Edição Análise de Imagens 

Este projeto foi desenvolvido como atividade prática da disciplina SIN392 - Processamento Digital de Imagens da Universidade Federal de Viçosa (UFV), sob orientação da Profª Drª João Fernando Mari. 

A aplicação permite o carregamento de imagens, aplicação de diversos filtros e transformações, operações morfológicas, segmentação com Otsu e visualização do histograma da imagem, tudo isso acessível por meio de uma interface web simples e funcional desenvolvida com Flask e OpenCV.

---

##  Funcionalidades

- Upload de imagens nos formatos `.jpg` ou `.png`
- Conversão automática para **escala de cinza**
- Redimensionamento de imagens grandes para manter a performance
- Aplicação de múltiplos filtros e transformações:
  - Na imagem original
  - Ou na última imagem processada
- Visualização da imagem original e da imagem processada lado a lado
- Exibição gráfica do histograma da imagem atual

---

##  Filtros e Processamentos Disponíveis

### Filtros Espaciais
- Média
- Mediana
- Gaussiano
- Máximo (Dilatação)
- Mínimo (Erosão)

### Filtros Passa-Alta
- Laplaciano
- Roberts
- Prewitt
- Sobel

### Filtros no Domínio da Frequência
- Passa-baixa (DFT)
- Passa-alta (DFT)

### Transformações de Intensidade
- Realce de Contraste
- Equalização de Histograma

### Operações Morfológicas
- Erosão
- Dilatação

### Segmentação
- Limiarização automática com método de Otsu

---

##  Como executar

### 1. Clone este repositório

```bash
git clone https://github.com/seu-usuario/editor-imagem-flask.git
cd editor-imagem-flask
````

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv

# No Windows:
venv\Scripts\activate

# No Linux/macOS:
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o sistema

```bash
python app.py
```

### 5. Acesse no navegador

```
http://localhost:5000
```

---

## Estrutura do Projeto

```
.
├── app.py                      # Lógica principal com rotas Flask
├── requirements.txt            # Lista de dependências
│
├── Processamento/              # Módulos de processamento de imagem
│   ├── filtros.py              # Filtros espaciais e frequência
│   ├── morfologia.py           # Erosão e dilatação
│   ├── segmentacao.py          # Otsu
│   ├── transformacoes.py       # Realce e equalização
│   ├── espectro_fourier.py     # (opcional) espectro de Fourier
│   └── histograma.py           # Cálculo do histograma
│
├── static/
│   ├── uploads/                # Imagens originais carregadas
│   ├── processing/             # Imagens processadas
│   └── histograma.png          # Gráfico de histograma gerado
│
├── templates/
│   ├── upload.html             # Página de upload
│   ├── processar.html          # Página de edição e filtros
│   └── histograma.html         # Página de histograma
```

---

## Notas Técnicas

*  O backend é construído com **Flask**
*  O processamento de imagem é realizado com **OpenCV**
*  Os histogramas são gerados com **Matplotlib**
*  Todas as imagens são convertidas para **escala de cinza**
*  Aplicação otimizada com **redimensionamento automático** (máximo de 800px de largura)

---


