import os
import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
RAINFOREST_API_KEY = os.getenv("RAINFOREST_API_KEY")

bot = telegram.Bot(token=TOKEN)

ASINS = [
    "B0C6VYG66P",
    "B09V3HN1XZ",
    "B09YVCDB7H"
]

def fetch_amazon_data(asin):
    url = "https://api.rainforestapi.com/request"
    params = {
        "api_key": RAINFOREST_API_KEY,
        "type": "product",
        "amazon_domain": "amazon.es",
        "asin": asin
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        product = data.get("product", {})
        title = product.get("title")
        price = product.get("buybox_winner", {}).get("price", {}).get("value")
        link = product.get("link")
        if title and price and link:
            return title, price, link
    except Exception as e:
        print(f"❌ Error fetching ASIN {asin}: {e}")
    return None

def notify_channel(products):
    for title, price, link in products:
        message = f"🔥 OFERTA: {title}\n💰 Precio: {price} €\n🔗 {link}"
        try:
            bot.send_message(chat_id=CHANNEL_ID, text=message)
        except Exception as e:
            print(f"❌ Error al enviar mensaje: {e}")

if __name__ == "__main__":
    print("📦 BOT_TOKEN:", "CARGADO" if TOKEN else "FALTA")
    print("📦 CHANNEL_ID:", CHANNEL_ID if CHANNEL_ID else "FALTA")
    print("📦 RAINFOREST_API_KEY:", "CARGADO" if RAINFOREST_API_KEY else "FALTA")

    ofertas = []
    for asin in ASINS:
        resultado = fetch_amazon_data(asin)
        if resultado:
            ofertas.append(resultado)

    if ofertas:
        notify_channel(ofertas)
    else:
        print("❌ No se encontraron productos.")
