import json
import socket
import time
from misurazione import crea_misurazione
from wifidc import connetti_wifi

# Connessione WiFi
connetti_wifi()

# Lettura configurazione camera
with open("configurazione.json") as f:
    config = json.load(f)

# Lettura parametri DA
with open("da.json") as f:
    da = json.load(f)

# Creazione socket
sock = socket.socket()

print("[DC] Connessione al server...")

sock.connect((da["IP"], da["porta"]))

print("[DC] Connesso al server")

while True:

    mis = crea_misurazione(config["camera"], config["ponte"])

    print("[DC] Misurazione:", mis)

    sock.send(json.dumps(mis).encode())

    time.sleep(5)