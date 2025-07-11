import os
import json
import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
RAINFOREST_API_KEY = os.getenv("RAINFOREST_API_KEY")

bot = telegram.Bot(token=TOKEN)

def scrape_amazon(asin_list):
    products = []
    for asin in asin_list:
        url = "https://api.rainforestapi.com/request"
        params = {
            "api_key": RAINFOREST_API_KEY,
            "type": "product",
            "amazon_domain": "amazon.es",
            "asin": asin
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            title = data.get("product", {}).get("title")
            price = data.get("product", {}).get("buybox_winner", {}).get("price", {}).get("value")

            if title and price:
                products.append({
                    "title": title,
                    "price": price,
                    "asin": asin
                })
            else:
                print(f"❌ No se encontró precio o título para {asin}")
        except Exception as e:
            print(f"❌ Error al obtener datos de {asin}: {e}")
    return products

def notify_channel(products):
    for p in products:
        message = f"🔥 OFERTA: {p['title']}\n💰 Precio: {p['price']} €\n🔗 Enlace: https://www.amazon.es/dp/{p['asin']}"
        try:
            bot.send_message(chat_id=CHANNEL_ID, text=message)
        except Exception as e:
            print(f"❌ Error al enviar mensaje: {e}")

if __name__ == "__main__":
    print("📦 BOT_TOKEN:", "CARGADO" if TOKEN else "FALTA")
    print("📦 CHANNEL_ID:", CHANNEL_ID if CHANNEL_ID else "FALTA")
    print("📦 RAINFOREST_API_KEY:", "CARGADO" if RAINFOREST_API_KEY else "FALTA")

    asin_list = ["B08CFSZLQ4", "B07PBF6DX5", "B08KH53NKR"]  # ASINs funcionales
    try:
        products = scrape_amazon(asin_list)
        if products:
            notify_channel(products)
        else:
            print("❌ No se encontraron productos.")
    except Exception as e:
        print("❌ Error general:", e)
