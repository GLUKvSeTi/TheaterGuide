import os
import requests
from bs4 import BeautifulSoup

url = 'https://lifemart.ru/ru/perm/catalog/blyuda'
response = requests.get(url)
print(response, response.text)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', class_='product-card')
    for product in products:
        product_name = product.find('div', class_='product-card__name').text.strip()
        product_price = product.find('div', class_='product-card__price').text.strip()
        print(f"{product_name} - {product_price}")
else:
    print(f"Error: {response.status_code} {response.text}")