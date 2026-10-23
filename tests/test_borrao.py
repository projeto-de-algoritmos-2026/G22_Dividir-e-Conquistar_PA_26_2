import numpy as np

from borrao import borrar_regiao, matriz_borrao


def test_linhas_da_matriz_somam_1():
    b = matriz_borrao(10, raio=3)
    assert np.allclose(b.sum(axis=1), 1)


def test_raio_zero_e_identidade():
    assert np.allclose(matriz_borrao(5, raio=0), np.eye(5))


def test_regiao_constante_continua_igual():
    imagem = np.full((40, 40, 3), 120, dtype=np.uint8)
    resultado = borrar_regiao(imagem, x=5, y=5, largura=20, altura=20, raio=4)
    assert np.array_equal(resultado, imagem)


def test_so_a_regiao_muda():
    rng = np.random.default_rng(0)
    imagem = rng.integers(0, 256, (50, 60, 3), dtype=np.uint8)
    resultado = borrar_regiao(imagem, x=10, y=20, largura=15, altura=10, raio=3)

    fora = np.ones(imagem.shape[:2], dtype=bool)
    fora[20:30, 10:25] = False
    assert np.array_equal(resultado[fora], imagem[fora])
    assert not np.array_equal(resultado[20:30, 10:25], imagem[20:30, 10:25])


def test_borrao_reduz_variacao():
    rng = np.random.default_rng(1)
    imagem = rng.integers(0, 256, (32, 32, 3), dtype=np.uint8)
    resultado = borrar_regiao(imagem, x=0, y=0, largura=32, altura=32, raio=5)
    assert resultado.std() < imagem.std()


def test_imagem_original_nao_e_alterada():
    imagem = np.zeros((10, 10, 3), dtype=np.uint8)
    imagem[5, 5] = 255
    copia = imagem.copy()
    borrar_regiao(imagem, x=0, y=0, largura=10, altura=10, raio=2)
    assert np.array_equal(imagem, copia)
