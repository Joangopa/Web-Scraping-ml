import asyncio
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import sqlite3
from telegram import Bot
import os
from dotenv import load_dotenv


load_dotenv()

# Configura bot telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)


def fetch_page():
    url="https://www.mercadolivre.com.br/tablet-samsung-galaxy-tab-s9-fe-wifi-128gb-6gb-ram-tela-imersiva-de-109/p/MLB29064087#polycard_client=search-nordic&wid=MLB5219065102&sid=search&searchVariation=MLB29064087&position=4&search_layout=grid&type=product&tracking_id=b2444a3a-bead-44c7-8690-24039bba3141"
    response = requests.get(url)
    return response.text

def parse_page(page_content):
    soup = BeautifulSoup(page_content, "html.parser")
    product_name = soup.find("h1", {"class": "ui-pdp-title"}).get_text()    
    prices = soup.find_all("span", {"class": "andes-money-amount__fraction"})
    old_price: int = int(prices[0].get_text().replace(".", ""))
    new_price: int = int(prices[1].get_text().replace(".", ""))
    installment_price: int = int(prices[2].get_text().replace(".", ""))

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    return {
        "product_name": product_name,
        "old_price": old_price,
        "new_price": new_price,
        "installment_price": installment_price,
        "timestamp": timestamp
    }

def create_connection(db_name="product_prices.db"):
    "Conexao ao banco de dados"
    conn = sqlite3.connect(db_name)
    return conn

def setup_database(conn):
    "Cria tabela para o banco de dados"
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            old_price INTEGER,
            new_price INTEGER,
            installment_price INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()


def save_to_database(conn, product_info):
    new_row = pd.DataFrame(product_info, index=[0])
    new_row.to_sql("product_prices", conn, if_exists="append", index=False)

def get_max_price(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(new_price) FROM product_prices")
    max_price = cursor.fetchone()[0]
    return max_price

async def send_telegram_message(message):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


async def main():
    
    conn = create_connection()
    setup_database(conn)

    while True:
        page_content = fetch_page()
        product_info = parse_page(page_content)

        max_price = get_max_price(conn)

        current_price = product_info["new_price"]
        
        if current_price > max_price:
            max_price = current_price
            print("Novo preço maior que o atual:", max_price)
            await send_telegram_message(f"Novo preco maior que o atual: {max_price}")
        else:
            print("Mesmo preço máximo:", max_price)
            await send_telegram_message(f"Mesmo preco maximo: {max_price}")

        save_to_database(conn, product_info)
        print("Dados salvos:", product_info)
        
        # aguarda 10 segundos
        await asyncio.sleep(10)
    
    #fecha conexao ao banco de dados
    conn.close()
 
asyncio.run(main())
