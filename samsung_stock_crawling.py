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

# 각 인덱스에 따른 데이터값

# 날짜
date_find = soup.select(".gray03")
date = []
for i in date_find:
    date.append(i.text)

# 수치데이터
num_data_find = soup.select("tr > .num > span.p11")
value_result = []
for i in num_data_find:
    value_result.append(i.text)

price_highlow = [] # 전일비 상승/하락
highlow_find = soup.select(".num > img")
for i in highlow_find:
    price_highlow.append(i.attrs["alt"])
# 수치데이터 => index번호 % 6 == (0): 종가, (1): 전일비, (2): 시가, (3): 고가, (4): 저가, (5): 거래량
end_price = [] # 종가
price_per_yesterday = [] # 전일비
start_price = [] # 시가
top_price = [] # 고가
below_price = [] # 저가
trade_num = [] # 거래량
for idx, val in enumerate(value_result):
    if idx % 6 == 0:
        end_price.append(val)
    elif idx % 6 == 1:
        price_per_yesterday.append(val.strip())
    elif idx % 6 == 2:
        start_price.append(val)
    elif idx % 6 == 3:
        top_price.append(val)
    elif idx % 6 == 4:
        below_price.append(val)
    else:
        trade_num.append(val)
# 전일비 통합
complete_per_yesterday = []
for i, j in zip(price_highlow, price_per_yesterday):
    complete_per_yesterday.append("(" + i + ")" + str(j))

# csv 작성하기
import csv

f = open("samsung_stock.csv", "w", newline="", encoding = "utf-8")
wr = csv.writer(f)
wr.writerow(index)
csv_value = []
for i in range(len(date)):
    temp = []
    temp.append(date[i])
    temp.append(end_price[i])
    temp.append(complete_per_yesterday[i])
    temp.append(start_price[i])
    temp.append(top_price[i])
    temp.append(below_price[i])
    temp.append(trade_num[i])
    csv_value.append(temp)

for i in csv_value:
    wr.writerow(i)
f.close()

# csv 읽기
f = open("samsung_stock.csv", "r", encoding = "utf-8")
reader = csv.reader(f)
data = list(reader)
print(data)