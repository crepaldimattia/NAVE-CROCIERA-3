import random

def leggi_dati():
    temperatura = round(random.uniform(18, 26), 2)
    umidita = round(random.uniform(45, 70), 2)
    return temperatura, umidita