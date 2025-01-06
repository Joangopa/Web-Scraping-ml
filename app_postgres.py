import asyncio
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import sqlite3
from telegram import Bot
import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine

load_dotenv()

# Configura bot telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

# configuracao do banco de dados PostgreSQL
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST =  os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

#cria o engine do SQLAlchemy para PostgreSQL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)

def fetch_page():
    url = "https://www.mercadolivre.com.br/tablet-samsung-galaxy-tab-s6-lite-2024-64gb-4gb-ram-wifi-cor-rosa/p/MLB35477124#polycard_client=search-nordic&wid=MLB4799262148&sid=search&searchVariation=MLB35477124&position=7&search_layout=grid&type=product&tracking_id=e717c71a-d935-45ea-967f-57e411ed29f0"
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

def create_connection():
    "Conexao ao banco de dados POSTGRESQL"
    conn = psycopg2.connect(
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    return conn

def setup_database(conn):
    "Cria tabela para o banco de dados"
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tabs6lite_prices (
            id SERIAL PRIMARY KEY,
            product_name TEXT,
            old_price INTEGER,
            new_price INTEGER,
            installment_price INTEGER,
            timestamp TEXT
        ) 
    """)
    conn.commit()
    cursor.close() 


def save_to_database(product_info):
    new_row = pd.DataFrame(product_info, index=[0])
    new_row.to_sql("tabs6lite_prices", engine, if_exists="append", index=False)

def get_max_price(conn):
    "Retorna o preco mais alto registrado até o momento"
    cursor = conn.cursor()
    cursor.execute("""
        SELECT new_price, timestamp
        FROM tabs6lite_prices
        WHERE new_price = (SELECT MAX(new_price) FROM tabS6lite_prices);
    """)
    result = cursor.fetchone()
    cursor.close()
    if result and result[0] is not None:
        return result[0]#, result[1]
    else:
        return None#, None

async def send_telegram_message(message):
    "envia mensagem ao bot telegram"
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


async def main():
    conn = create_connection()
    setup_database(conn)

    while True:
        page_content = fetch_page()
        product_info = parse_page(page_content)
        current_price = product_info["new_price"]
        
        max_price = get_max_price(conn)

        # comparação de preços
        if max_price is None or current_price > max_price:
            max_price = current_price
            print("Novo preço maior que o atual:", max_price)
            await send_telegram_message(f"Novo preco maior que o atual: {max_price}")
        else:
            print("Mesmo preço máximo:", max_price)
            await send_telegram_message(f"Mesmo preco maximo: {max_price}")

        save_to_database(product_info)
        print("Dados salvos:", product_info)
        
        # aguarda 10 segundos
        await asyncio.sleep(10)
    
    #fecha conexao ao banco de dados
    conn.close()
 
asyncio.run(main())
