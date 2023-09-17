import requests
from bs4 import BeautifulSoup

# response = requests.get("https://finance.naver.com/item/sise.nhn?code=005930")
response = requests.get("https://finance.naver.com/item/sise_day.naver?code=005930&page=1", headers={"User-agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text,'html.parser')

# csv index 항목 크롤링
index_find = soup.select("table > tr > th")
index = [] # csv의 index 항목에 대한 리스트
for i in index_find:
    index.append(i.text)

print("csv 인덱스: ", index)
# 각 인덱스에 따른 데이터값

# 날짜
date_find = soup.select(".gray03")
date = []
for i in date_find:
    date.append(i.text)

print("날짜: ", date)

# 종가
endprice_find = soup.select("tr > .num > span.p11")
endprice = []
for i in endprice_find:
    endprice.append(i.text)

print("종가: ", endprice)