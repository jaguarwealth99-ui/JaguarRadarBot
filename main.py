
import requests
import time

# ==========================
# CONFIGURACIÓN
# ==========================
TELEGRAM_TOKEN = "8240643982:AAFsiRGL6g39mxHZG17gQ5Br80UlmpRC9gY"
CHAT_ID = "1653670370"
INTERVALO_SEGUNDOS = 60  # Intervalo de búsqueda en segundos

# ==========================
# FUNCIONES
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
        holders = pair.get("txns", {}).get("h24", {}).get("buys", 0) + pair.get("txns", {}).get("h24", {}).get("sells", 0)

        # ===== FILTROS JAGUAR =====
        if mcap > 50000:
            return False
        if volumen < mcap:
            return False
        if liquidez < 2000:
            return False
        if holders < 20:
            return False

        return True
    except:
        return False

def escanear_red(red):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{red}"
    r = requests.get(url)
    data = r.json()
    return data.get("pairs", [])

# ==========================
# LOOP PRINCIPAL
# ==========================
enviar_alerta("🚀 Jaguar Cazador Patrón TROLL conectado y listo para cazar gemas 🐆💎")

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

                mensaje = f"🚀 <b>Nuevo posible Jaguar</b>\n"                           f"🌐 Red: {red}\n"                           f"🏷 {nombre} ({simbolo})\n"                           f"💰 MCAP: ${mcap}\n"                           f"📊 Volumen 24h: ${volumen}\n"                           f"🔗 {enlace}"
                enviar_alerta(mensaje)
    time.sleep(INTERVALO_SEGUNDOS)
