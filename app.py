import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


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

def save_to_dataframe(product_info, df):
    new_row = pd.DataFrame(product_info, index=[0])
    df = pd.concat([df, new_row], ignore_index=True)
    return df

if __name__ == "__main__":

    df = pd.DataFrame()
    while True:
        page_content = fetch_page()
        product_info = parse_page(page_content)
        df = save_to_dataframe(product_info, df)
        print(df)
        time.sleep(10)
