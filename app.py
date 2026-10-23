import io
import time

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw

from borrao import borrar_regiao
from strassen import multiplicacao_classica, strassen

LARGURA_MAXIMA = 600


def carregar_imagem(arquivo):
    imagem = Image.open(arquivo).convert("RGB")
    if imagem.width > LARGURA_MAXIMA:
        altura = round(imagem.height * LARGURA_MAXIMA / imagem.width)
        imagem = imagem.resize((LARGURA_MAXIMA, altura))
    return np.array(imagem)


def desenhar_retangulo(imagem, x, y, largura, altura):
    marcada = Image.fromarray(imagem)
    ImageDraw.Draw(marcada).rectangle(
        (x, y, x + largura - 1, y + altura - 1), outline=(255, 0, 0), width=3
    )
    return marcada


def medir(funcao, a, b, corte):
    contador = {"multiplicacoes": 0}
    inicio = time.perf_counter()
    funcao(a, b, corte=corte, contador=contador)
    return time.perf_counter() - inicio, contador["multiplicacoes"]


st.set_page_config(page_title="Censurador Strassen", layout="wide")
st.title("Censurador Strassen")
st.caption("Borra rostos multiplicando matrizes com o algoritmo de Strassen.")

arquivo = st.file_uploader("Foto", type=["png", "jpg", "jpeg"])
if arquivo is None:
    st.info("Envie uma foto para começar.")
    st.stop()

imagem = carregar_imagem(arquivo)
altura_img, largura_img = imagem.shape[:2]

st.sidebar.header("Região do rosto")
x = st.sidebar.slider("x", 0, largura_img - 1, largura_img // 3)
y = st.sidebar.slider("y", 0, altura_img - 1, altura_img // 4)
largura = st.sidebar.slider("Largura", 1, largura_img - x, min(largura_img // 3, largura_img - x))
altura = st.sidebar.slider("Altura", 1, altura_img - y, min(altura_img // 3, altura_img - y))

st.sidebar.header("Borrão")
raio = st.sidebar.slider("Intensidade (raio da média)", 1, 40, 12)
corte = st.sidebar.select_slider("Caso base do Strassen (lado)", [1, 2, 4, 8, 16, 32, 64], 16)

contador = {"multiplicacoes": 0}
inicio = time.perf_counter()
borrada = borrar_regiao(imagem, x, y, largura, altura, raio, corte, contador)
tempo = time.perf_counter() - inicio

col_original, col_borrada = st.columns(2)
col_original.image(desenhar_retangulo(imagem, x, y, largura, altura), caption="Original")
col_borrada.image(borrada, caption="Borrada")

buffer = io.BytesIO()
Image.fromarray(borrada).save(buffer, format="PNG")
st.download_button("Baixar imagem borrada", buffer.getvalue(), "borrada.png", "image/png")

st.subheader("Strassen x dividir e conquistar clássico")
st.write(
    f"O borrão fez 6 produtos de matrizes (2 por canal de cor) em **{tempo * 1000:.0f} ms**, "
    f"com **{contador['multiplicacoes']}** multiplicações no caso base."
)

lado = st.select_slider("Lado das matrizes de teste", [64, 128, 256, 512], 256)
if st.button("Comparar"):
    rng = np.random.default_rng(0)
    a = rng.random((lado, lado))
    b = rng.random((lado, lado))
    tempo_s, mult_s = medir(strassen, a, b, corte)
    tempo_c, mult_c = medir(multiplicacao_classica, a, b, corte)

    col1, col2 = st.columns(2)
    col1.metric("Strassen (7 subproblemas)", f"{tempo_s * 1000:.0f} ms", f"{mult_s} multiplicações", delta_color="off")
    col2.metric("Clássico (8 subproblemas)", f"{tempo_c * 1000:.0f} ms", f"{mult_c} multiplicações", delta_color="off")
    st.caption(
        f"Com lado {lado} e caso base {corte}, a recursão tem log2({lado}/{corte}) níveis: "
        f"Strassen faz 7 chamadas por nível e o clássico faz 8."
    )
