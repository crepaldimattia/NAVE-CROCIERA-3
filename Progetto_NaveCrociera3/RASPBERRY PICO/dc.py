import socket
import json
import time
from wifidc import connetti_wifi
from misurazione import leggi_dati

# Connessione WiFi
connetti_wifi()

# Lettura configurazioni
with open("da.json") as f:
    da = json.load(f)

with open("configurazione.json") as f:
    config = json.load(f)

# Connessione al DA
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((da["IP"], da["porta"]))
print("[DC] Connesso al DA")

# Riceve TEMPO_RILEVAZIONE dal DA
tempo_rilevazione = int(sock.recv(1024).decode())
print("[DC] Tempo rilevazione:", tempo_rilevazione, "secondi")

rilevazione = 0

while True:
    rilevazione += 1
    temperatura, umidita = leggi_dati()

    iotdata = {
        "camera": config["camera"],
        "ponte": config["ponte"],
        "sensore": config["sensore"],
        "identita": config["identita"],
        "osservazione": {
            "rilevazione": rilevazione,
            "temperatura": temperatura,
            "umidita": umidita,
            "timestamp": int(time.time())
        }
    }

    messaggio = json.dumps(iotdata)
    sock.send(messaggio.encode())

    print("[DC] Inviato:", messaggio)
    time.sleep(tempo_rilevazione)