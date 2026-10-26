import numpy as np

from strassen import strassen


def matriz_borrao(n, raio):
    """Matriz n x n em que cada linha tira a média dos vizinhos a até `raio` posições."""
    b = np.zeros((n, n))
    for i in range(n):
        inicio = max(0, i - raio)
        fim = min(n, i + raio + 1)
        b[i, inicio:fim] = 1 / (fim - inicio)
    return b


def borrar_regiao(imagem, x, y, largura, altura, raio, corte=64, contador=None):
    """Borra o retângulo (x, y, largura, altura) da imagem RGB com B_altura · R · B_largura^T."""
    resultado = imagem.copy()
    regiao = imagem[y : y + altura, x : x + largura].astype(float)
    b_linhas = matriz_borrao(regiao.shape[0], raio)
    b_colunas = matriz_borrao(regiao.shape[1], raio)

    for canal in range(regiao.shape[2]):
        borrado = strassen(b_linhas, regiao[:, :, canal], corte, contador)
        borrado = strassen(borrado, b_colunas.T, corte, contador)
        resultado[y : y + altura, x : x + largura, canal] = np.clip(np.rint(borrado), 0, 255)
    return resultado
