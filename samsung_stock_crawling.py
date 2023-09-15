import requests
from bs4 import BeautifulSoup

# response = requests.get("https://finance.naver.com/item/sise.nhn?code=005930")
response = requests.get("https://finance.naver.com/item/sise_day.naver?code=005930&page=1", headers={"User-agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text,'html.parser')
print(soup)
