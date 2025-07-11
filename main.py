import os
import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
RAINFOREST_API_KEY = os.getenv("RAINFOREST_API_KEY")

bot = telegram.Bot(token=TOKEN)

SEARCH_TERMS = [
    "monitor gaming", "ssd barato", "portátil oferta", "ratón inalámbrico", "teclado mecánico",
    "auriculares bluetooth", "powerbank", "tarjeta gráfica", "ofertas tecnología", "smartwatch barato"
]

def search_amazon_products():
    results = []
    headers = {"Content-Type": "application/json"}
    for term in SEARCH_TERMS:
        params = {
            "api_key": RAINFOREST_API_KEY,
            "type": "search",
            "amazon_domain": "amazon.es",
            "search_term": term
        }
        try:
            response = requests.get("https://api.rainforestapi.com/request", headers=headers, params=params)
            data = response.json()

            if "search_results" in data and data["search_results"]:
                first = data["search_results"][0]
                title = first.get("title", "Sin título")
                price_info = first.get("price", {})
                price = price_info.get("value", None)
                link = first.get("link", "#")

                if title and price:
                    results.append((title, price, link))
                else:
                    print(f"❌ No se encontró precio o título para término: {term}")
            else:
                print(f"❌ No se encontraron resultados para: {term}")

        except Exception as e:
            print(f"❌ Error buscando '{term}': {e}")
    return results

def notify_channel(products):
    for title, price, url in products:
        message = f"🔥 OFERTA DETECTADA:
📦 {title}
💰 {price} €
🔗 {url}"
        try:
            bot.send_message(chat_id=CHANNEL_ID, text=message)
        except Exception as e:
            print(f"❌ Error al enviar mensaje: {e}")

if __name__ == "__main__":
    print("📦 BOT_TOKEN:", "CARGADO" if TOKEN else "FALTA")
    print("📦 CHANNEL_ID:", CHANNEL_ID if CHANNEL_ID else "FALTA")
    print("📦 RAINFOREST_API_KEY:", "CARGADO" if RAINFOREST_API_KEY else "FALTA")

    try:
        productos = search_amazon_products()
        if productos:
            notify_channel(productos)
        else:
            print("❌ No se encontraron productos.")
    except Exception as e:
        print("❌ Error general:", e)