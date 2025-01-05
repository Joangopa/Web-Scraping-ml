import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import sqlite3

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

def create_connection(db_name="tabS6lite_prices.db"):
    "Conexao ao banco de dados"
    conn = sqlite3.connect(db_name)
    return conn

def setup_database(conn):
    "Cria tabela para o banco de dados"
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tabS6lite_prices (
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
    new_row.to_sql("tabS6lite_prices", conn, if_exists="append", index=False)

if __name__ == "__main__":

    conn = create_connection()
    setup_database(conn)

    df = pd.DataFrame()
    while True:
        page_content = fetch_page()
        product_info = parse_page(page_content)
        save_to_database(conn, product_info)
        print("Dados salvos:", product_info)
        time.sleep(10)
