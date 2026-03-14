import network
import json
import time

def connetti_wifi():

    with open("wifipico.json") as f:
        wifi = json.load(f)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.connect(wifi["ssid"], wifi["pw"])

    while not wlan.isconnected():
        print("Connessione al WiFi...")
        time.sleep(1)

    print("WiFi connesso:", wlan.ifconfig())