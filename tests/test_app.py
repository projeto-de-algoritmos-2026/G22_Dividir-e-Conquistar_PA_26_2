import io
from unittest.mock import patch

import numpy as np
from PIL import Image
from streamlit.testing.v1 import AppTest


def _foto():
    rng = np.random.default_rng(0)
    pixels = rng.integers(0, 256, (120, 160, 3), dtype=np.uint8)
    buffer = io.BytesIO()
    Image.fromarray(pixels).save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def test_sem_foto_pede_upload():
    app = AppTest.from_file("app.py").run()
    assert not app.exception
    assert "Envie uma foto" in app.info[0].value


def test_com_foto_borra_e_compara():
    with patch("streamlit.file_uploader", return_value=_foto()):
        app = AppTest.from_file("app.py", default_timeout=30).run()
        assert not app.exception
        assert len(app.metric) == 0

        app.select_slider[1].set_value(64)
        app.button[0].click().run()
        assert not app.exception
        assert len(app.metric) == 2
