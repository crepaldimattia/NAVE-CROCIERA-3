import socket
import json
import time
from cripta import cripta

# Lettura parametri
with open("parametri.json") as f:
    p = json.load(f)

# Creazione server TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((p["IP_SERVER"], p["PORTA_SERVER"]))
server.listen(1)

print("[DA] Server avviato, in attesa del DC...")
conn, addr = server.accept()
print("[DA] DC connesso:", addr)

# Invia TEMPO_RILEVAZIONE al DC
conn.send(str(p["TEMPO_RILEVAZIONE"]).encode())

temperature = []
umidita = []
invio_numero = 0
ultimo_invio = time.time()

try:
    while True:
        data = conn.recv(4096).decode()
        if not data:
            break

        iot = json.loads(data)
        print("[DA] Ricevuto:", iot)

        temperature.append(iot["osservazione"]["temperatura"])
        umidita.append(iot["osservazione"]["umidita"])

        if time.time() - ultimo_invio >= p["TEMPO_INVIO"]:
            invio_numero += 1

            risultato = {
                "camera": iot["camera"],
                "ponte": iot["ponte"],
                "temperaturam": round(sum(temperature) / len(temperature), p["N_DECIMALI"]),
                "umiditam": round(sum(umidita) / len(umidita), p["N_DECIMALI"]),
                "dataeora": int(time.time()),
                "invionumero": invio_numero,
                "identita": p["IDENTITA_GIOT"]
            }

            risultato = cripta(risultato)

            print("[DA] Inviato a piattaforma:", risultato)

            # MEMORIZZAZIONE CORRETTA COME DA PDF
            with open("iotp/db.json", "a") as db:
                db.write(json.dumps(risultato, indent=2))
                db.write("\n")

            temperature.clear()
            umidita.clear()
            ultimo_invio = time.time()

except KeyboardInterrupt:
    print("\n[DA] Arresto manuale")
    print("[DA] Numero invii totali:", invio_numero)