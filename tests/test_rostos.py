from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from rostos import detectar_rostos

PASTA = Path(__file__).parent.parent / "imagens_teste"
LARGURA_MAXIMA = 600  # mesma largura que o app usa ao carregar a foto

# Beatles tem 5: os 4 da banda e o rosto cortado no canto superior esquerdo.
# Aldrin tem 1 falso positivo conhecido: o visor do capacete (confiança 0,78, acima
# de rostos reais da Solvay, então não dá para cortar pelo limiar).
# Migrant Mother tem 1: as duas crianças estão de costas.
ROSTOS_ESPERADOS = {
    "aldrin_visor.jpg": 1,
    "apollo11.jpg": 3,
    "audrey.jpg": 1,
    "einstein_chaplin.jpg": 2,
    "einstein_tongue.jpg": 1,
    "everest_sem_rosto.jpg": 0,
    "frida.jpg": 1,
    "gandhi.jpg": 1,
    "gato_sem_rosto.jpg": 0,
    "migrant_mother.jpg": 1,
    "nefertiti_perfil.jpg": 1,
    "beatles.jpg": 5,
    "curie.jpg": 1,
    "einstein.jpg": 1,
    "lincoln.jpg": 1,
    "moca_pearl.jpg": 1,
    "mona_lisa.jpg": 1,
    "obama_familia.jpg": 4,
    "solvay_grupo.jpg": 29,
    "van_gogh.jpg": 1,
}


def _carregar(nome):
    imagem = Image.open(PASTA / nome).convert("RGB")
    altura = round(imagem.height * LARGURA_MAXIMA / imagem.width)
    return np.array(imagem.resize((LARGURA_MAXIMA, altura)))


@pytest.mark.parametrize("nome, esperado", ROSTOS_ESPERADOS.items())
def test_conta_rostos_das_imagens_de_teste(nome, esperado):
    assert len(detectar_rostos(_carregar(nome))) == esperado


def test_regioes_ficam_dentro_da_imagem():
    imagem = _carregar("beatles.jpg")
    altura, largura = imagem.shape[:2]
    for x, y, w, h in detectar_rostos(imagem):
        assert 0 <= x and 0 <= y and w > 0 and h > 0
        assert x + w <= largura and y + h <= altura


def test_imagem_sem_rosto():
    assert detectar_rostos(np.zeros((120, 160, 3), np.uint8)) == []
