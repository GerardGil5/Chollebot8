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

def get_product_info(asin):
    url = "https://api.rainforestapi.com/request"
    params = {
        "api_key": RAINFOREST_API_KEY,
        "type": "product",
        "amazon_domain": "amazon.es",
        "asin": asin
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        title = data.get("product", {}).get("title")
        price = data.get("product", {}).get("buybox_winner", {}).get("price", {}).get("value")
        link = f"https://www.amazon.es/dp/{asin}"
        
        if title and price:
            return {
                "title": title,
                "price": price,
                "url": link
            }
        else:
            print(f"❌ No se encontró precio o título para {asin}")
            return None

    except Exception as e:
        print(f"❌ Error al obtener info de {asin}: {e}")
        return None

def notify_channel(products):
    for product in products:
        title = product["title"]
        price = product["price"]
        url = product["url"]

        message = f"🔥 OFERTA: {title}\n💰 Precio: {price} €\n🔗 Enlace: {url}"

        try:
            bot.send_message(chat_id=CHANNEL_ID, text=message)
        except Exception as e:
            print(f"❌ Error al enviar mensaje: {e}")

if __name__ == "__main__":
    print("📦 BOT_TOKEN:", "CARGADO" if TOKEN else "FALTA")
    print("📦 CHANNEL_ID:", CHANNEL_ID if CHANNEL_ID else "FALTA")
    print("📦 RAINFOREST_API_KEY:", "CARGADO" if RAINFOREST_API_KEY else "FALTA")

    asin_list = ["B09YVCDB7H", "B0C6VYG66P", "B0C2X8TVVV"]
    ofertas = []

    for asin in asin_list:
        info = get_product_info(asin)
        if info:
            ofertas.append(info)

    if ofertas:
        notify_channel(ofertas)
    else:
        print("❌ No se encontraron productos.")
