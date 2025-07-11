# -*- coding: utf-8 -*-
import os
import json
import requests
from bs4 import BeautifulSoup
import telegram
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telegram.Bot(token=TOKEN)

def scrape_amazon():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    urls = [
        "https://www.amazon.es/dp/B0C6VYG66P",
        "https://www.amazon.es/dp/B09V3HN1XZ",
        "https://www.amazon.es/dp/B09YVCDB7H"
    ]
    products = []
    for url in urls:
        try:
            page = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(page.content, "html.parser")
            title = soup.find(id="productTitle")
            price = soup.find("span", class_="a-price-whole")
            if title and price:
                title_text = title.get_text(strip=True)
                price_text = price.get_text(strip=True)
                products.append((title_text, price_text, url))
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
    return products

def notify_channel(products):
    for title, price, url in products:
        message = f"🔥 OFERTA: {title}\n💰 Precio: {price} €\n🔗 Enlace: {url}"
        try:
            bot.send_message(chat_id=CHANNEL_ID, text=message)
        except Exception as e:
            print(f"❌ Error al enviar mensaje: {e}")

if __name__ == "__main__":
    print("📦 BOT_TOKEN:", "CARGADO" if TOKEN else "FALTA")
    print("📦 CHANNEL_ID:", CHANNEL_ID if CHANNEL_ID else "FALTA")

    try:
        ofertas = scrape_amazon()
        if ofertas:
            notify_channel(ofertas)
        else:
            print("❌ No se encontraron productos.")
    except Exception as e:
        print("❌ Error general:", e)
