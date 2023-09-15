import requests
from bs4 import BeautifulSoup

response = requests.get("https://finance.naver.com/item/sise.nhn?code=005930")
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)