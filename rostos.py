from pathlib import Path

import cv2

# OpenCL trava o processo no Windows quando o detector roda fora da thread principal.
cv2.ocl.setUseOpenCL(False)

MODELO = Path(__file__).parent / "modelos" / "face_detection_yunet_2023mar.onnx"
CONFIANCA_MINIMA = 0.6

_detector = cv2.FaceDetectorYN.create(str(MODELO), "", (0, 0), CONFIANCA_MINIMA)


def detectar_rostos(imagem):
    """Retorna (x, y, largura, altura) de cada rosto da imagem RGB, usando a rede YuNet."""
    altura, largura = imagem.shape[:2]
    _detector.setInputSize((largura, altura))
    _, rostos = _detector.detect(cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR))
    if rostos is None:
        return []
    regioes = []
    for rosto in rostos:
        x, y, w, h = (int(v) for v in rosto[:4])
        x, y = max(0, x), max(0, y)
        regioes.append((x, y, min(w, largura - x), min(h, altura - y)))
    return regioes
