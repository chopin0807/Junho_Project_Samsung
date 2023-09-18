import requests
from bs4 import BeautifulSoup

# response = requests.get("https://finance.naver.com/item/sise.nhn?code=005930")
p = 0
date = []
index = ["날짜", "종가", "전일비", "시가", "고가", "저가", "거래량"]
price_highlow = [] # 전일비 상승/하락
end_price = [] # 종가
price_per_yesterday = [] # 전일비
start_price = [] # 시가
top_price = [] # 고가
below_price = [] # 저가
trade_num = [] # 거래량
highlow_find_result = []
while True:
    p += 1
    response = requests.get("https://finance.naver.com/item/sise_day.naver?code=005930&page="+str(p), headers={"User-agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text,'html.parser')
    # 8월 한달동안 크롤링하기 위한 조건생성
    index_find = soup.select("table > tr > th")
    date_find = soup.select(".gray03")
    num_data_find = soup.select("tr > .num > span.p11")
    highlow_find = soup.select(".num > img")

    for i in date_find:
        date.append(i.text)
    
    for a in highlow_find:
        highlow_find_result.append(a)
    
    value_data = []
    for num_data in num_data_find:
        value_data.append(num_data.text)

    for idx, val in enumerate(value_data):
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
 
    for i in date:
        pass

    if int(i.split(".")[0]) == 2023 and int(i.split(".")[1]) < 8:
        date_result = []
        value_data = []
        for val1 in date:

            if int(val1.split(".")[0]) == 2023 and int(val1.split(".")[1]) == 8:
                date_result.append(val1)
        break

line = 0
for i in price_per_yesterday:
        if i == '0':
            price_highlow.append("변동없음")
        else:
            price_highlow.append(highlow_find_result[line].attrs["alt"])
            line += 1

# 전일비 통합
complete_per_yesterday = []
for i, j in zip(price_highlow, price_per_yesterday):
    complete_per_yesterday.append("(" + i + ")" + str(j))
# csv 작성하기
import csv

f = open("stock.csv", "w", newline="", encoding = "utf-8")
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

import pandas as pd
df = pd.read_csv("stock.csv", encoding="utf-8")
print(df)
print(len(df))
print(df.loc[1])
print(df["날짜"][0].split("."))

for dn in range(len(df)):
    if df["날짜"][dn].split(".")[0] == "2023" and df["날짜"][dn].split(".")[1] == "08":
        pass
    else:
        df.drop([dn], axis=0, inplace=True)

print(df)
df.to_csv("stock.csv")