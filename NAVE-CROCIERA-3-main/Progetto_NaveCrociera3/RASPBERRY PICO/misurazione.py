import random
import time

def crea_misurazione(camera, ponte):

    temperatura = random.uniform(18, 28)
    umidita = random.uniform(30, 70)

    misurazione = {
        "camera": camera,
        "ponte": ponte,
        "osservazione": {
            "temperatura": round(temperatura, 2),
            "umidita": round(umidita, 2)
        },
        "dataeora": int(time.time())
    }

    return misurazione