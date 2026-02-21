import json
import time

def connetti_wifi():
    with open("wifipico.json") as f:
        wifi = json.load(f)

    print("[DC] Connessione WiFi a", wifi["ssid"])
    time.sleep(1)
    print("[DC] WiFi connesso")