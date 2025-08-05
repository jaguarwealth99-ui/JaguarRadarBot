import requests
import time
import os
import threading
from flask import Flask

# ==========================
# CONFIGURACIÓN
# ==========================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
INTERVALO_SEGUNDOS = 10800  # Cada 3 horas

# ==========================
# BOT FUNCTIONS
# ==========================
def enviar_alerta(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Error enviando alerta:", e)

def cumple_filtros(pair):
    try:
        mcap = pair.get("fdv", 0)
        volumen = pair.get("volume", {}).get("h24", 0)
        liquidez = pair.get("liquidity", {}).get("usd", 0)
        buys = pair.get("txns", {}).get("h24", {}).get("buys", 0)
        sells = pair.get("txns", {}).get("h24", {}).get("sells", 0)
        holders = buys + sells

        if mcap <= 0 or mcap > 50000:
            return False
        if liquidez < 2000:
            return False
        if volumen < mcap:
            return False
        if holders < 20:
            return False

        price_change = pair.get("priceChange", {}).get("h24", 0)
        if price_change > 50:
            return False

        return True
    except:
        return False

def escanear_red(red):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{red}"
    r = requests.get(url)
    data = r.json()
    return data.get("pairs", [])

def bot_loop():
    enviar_alerta("🚀 Jaguar Cazador Patrón TROLL conectado y listo 🐆💎")
    while True:
        print("⏳ Escaneando nuevos tokens...")
        for red in ["solana", "base"]:
            tokens = escanear_red(red)
            for t in tokens:
                if cumple_filtros(t):
                    nombre = t["baseToken"]["name"]
                    simbolo = t["baseToken"]["symbol"]
                    mcap = t.get("fdv", 0)
                    volumen = t.get("volume", {}).get("h24", 0)
                    enlace = t.get("url", "")
                    price_change = t.get("priceChange", {}).get("h24", 0)

                    mensaje = (
                        f"🚀 <b>Nuevo posible Jaguar</b> 🐆💎\n"
                        f"🌐 Red: {red}\n"
                        f"🏷 {nombre} ({simbolo})\n"
                        f"💰 MCAP: ${mcap}\n"
                        f"📊 Volumen 24h: ${volumen}\n"
                        f"📈 Cambio 24h: {price_change}%\n"
                        f"🔗 {enlace}"
                    )
                    enviar_alerta(mensaje)
        time.sleep(INTERVALO_SEGUNDOS)

# ==========================
# FLASK SERVER
# ==========================
app = Flask(__name__)

@app.route('/')
def home():
    return "Jaguar Bot corriendo 🐆💎"

if __name__ == '__main__':
    threading.Thread(target=bot_loop).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
