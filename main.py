import os
import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
RAINFOREST_API_KEY = os.getenv("RAINFOREST_API_KEY")

bot = telegram.Bot(token=TOKEN)

def get_amazon_products():
    asin_list = ["B09V3HN1XZ", "B09YVCDB7H", "B0C6VYG66P"]  # productos reales y en stock
    headers = {"Content-Type": "application/json"}
    products = []

    for asin in asin_list:
        params = {
            "api_key": RAINFOREST_API_KEY,
            "type": "product",
            "amazon_domain": "amazon.es",
            "asin": asin
        }
        try:
            response = requests.get("https://api.rainforestapi.com/request", params=params, headers=headers, timeout=10)
            data = response.json()
            product = data.get("product", {})

            title = product.get("title")
            price_data = product.get("buybox_winner", {}).get("price", {})
            price = price_data.get("value")

            if title and price:
                link = f"https://www.amazon.es/dp/{asin}"
                products.append((title, price, link))
            else:
                print(f"❌ No se encontró precio o título para {asin}")
        except Exception as e:
            print(f"❌ Error con el ASIN {asin}: {e}")
    return products

def notify_channel(products):
    for title, price, url in products:
        message = f"🔥 OFERTA: {title}\n💰 Precio: {price} €\n🔗 Enlace: {url}"
        try:
            bot.send_message(chat_id=CHANNEL_ID, text=message)
            print(f"✅ Enviado: {title}")
        except Exception as e:
            print(f"❌ Error al enviar mensaje: {e}")

if __name__ == "__main__":
    print("📦 BOT_TOKEN:", "CARGADO" if TOKEN else "FALTA")
    print("📦 CHANNEL_ID:", CHANNEL_ID if CHANNEL_ID else "FALTA")
    print("📦 RAINFOREST_API_KEY:", "CARGADO" if RAINFOREST_API_KEY else "FALTA")

    try:
        ofertas = get_amazon_products()
        if ofertas:
            notify_channel(ofertas)
        else:
            print("❌ No se encontraron productos.")
    except Exception as e:
        print("❌ Error general:", e)
