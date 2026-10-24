import numpy as np
import pytest

from strassen import multiplicacao_classica, strassen


@pytest.mark.parametrize("n", [1, 2, 3, 7, 16, 33, 100])
def test_strassen_igual_ao_numpy(n):
    rng = np.random.default_rng(n)
    a = rng.random((n, n))
    b = rng.random((n, n))
    assert np.allclose(strassen(a, b, corte=4), a @ b)


def test_strassen_matrizes_retangulares():
    rng = np.random.default_rng(0)
    a = rng.random((5, 12))
    b = rng.random((12, 3))
    resultado = strassen(a, b, corte=2)
    assert resultado.shape == (5, 3)
    assert np.allclose(resultado, a @ b)


def test_strassen_dimensoes_incompativeis():
    with pytest.raises(ValueError):
        strassen(np.ones((2, 3)), np.ones((2, 3)))


def test_classica_igual_ao_numpy():
    rng = np.random.default_rng(1)
    a = rng.random((20, 20))
    b = rng.random((20, 20))
    assert np.allclose(multiplicacao_classica(a, b, corte=4), a @ b)


def test_strassen_faz_7_chamadas_por_nivel():
    contador = {"multiplicacoes": 0}
    strassen(np.ones((4, 4)), np.ones((4, 4)), corte=1, contador=contador)
    assert contador["multiplicacoes"] == 49


def test_classica_faz_8_chamadas_por_nivel():
    contador = {"multiplicacoes": 0}
    multiplicacao_classica(np.ones((4, 4)), np.ones((4, 4)), corte=1, contador=contador)
    assert contador["multiplicacoes"] == 64
