import numpy as np


def _proxima_potencia_de_2(n):
    potencia = 1
    while potencia < n:
        potencia *= 2
    return potencia


def _completar(matriz, tamanho):
    completa = np.zeros((tamanho, tamanho), dtype=float)
    completa[: matriz.shape[0], : matriz.shape[1]] = matriz
    return completa


def _dividir(m):
    meio = m.shape[0] // 2
    return m[:meio, :meio], m[:meio, meio:], m[meio:, :meio], m[meio:, meio:]


def _juntar(c11, c12, c21, c22):
    return np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))


def _strassen(a, b, corte, contador):
    if a.shape[0] <= corte:
        contador["multiplicacoes"] += 1
        return a @ b

    a11, a12, a21, a22 = _dividir(a)
    b11, b12, b21, b22 = _dividir(b)

    m1 = _strassen(a11 + a22, b11 + b22, corte, contador)
    m2 = _strassen(a21 + a22, b11, corte, contador)
    m3 = _strassen(a11, b12 - b22, corte, contador)
    m4 = _strassen(a22, b21 - b11, corte, contador)
    m5 = _strassen(a11 + a12, b22, corte, contador)
    m6 = _strassen(a21 - a11, b11 + b12, corte, contador)
    m7 = _strassen(a12 - a22, b21 + b22, corte, contador)

    c11 = m1 + m4 - m5 + m7
    c12 = m3 + m5
    c21 = m2 + m4
    c22 = m1 - m2 + m3 + m6
    return _juntar(c11, c12, c21, c22)


def _classica(a, b, corte, contador):
    if a.shape[0] <= corte:
        contador["multiplicacoes"] += 1
        return a @ b

    a11, a12, a21, a22 = _dividir(a)
    b11, b12, b21, b22 = _dividir(b)

    c11 = _classica(a11, b11, corte, contador) + _classica(a12, b21, corte, contador)
    c12 = _classica(a11, b12, corte, contador) + _classica(a12, b22, corte, contador)
    c21 = _classica(a21, b11, corte, contador) + _classica(a22, b21, corte, contador)
    c22 = _classica(a21, b12, corte, contador) + _classica(a22, b22, corte, contador)
    return _juntar(c11, c12, c21, c22)


def _multiplicar(recursao, a, b, corte, contador):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape[1] != b.shape[0]:
        raise ValueError(f"dimensões incompatíveis: {a.shape} x {b.shape}")
    if contador is None:
        contador = {"multiplicacoes": 0}

    tamanho = _proxima_potencia_de_2(max(*a.shape, *b.shape))
    resultado = recursao(_completar(a, tamanho), _completar(b, tamanho), corte, contador)
    return resultado[: a.shape[0], : b.shape[1]]


def strassen(a, b, corte=64, contador=None):
    """Multiplica a e b com Strassen: 7 subproblemas de metade do tamanho.

    Matrizes de lado <= corte são multiplicadas direto no caso base.
    """
    return _multiplicar(_strassen, a, b, corte, contador)


def multiplicacao_classica(a, b, corte=64, contador=None):
    """Dividir e conquistar sem o truque de Strassen: 8 subproblemas."""
    return _multiplicar(_classica, a, b, corte, contador)
