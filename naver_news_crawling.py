# 네이버 뉴스 크롤링
# 20230930 ~ 20230901까지의 각 URL로 접속한 후 각 기사에 접속하는 방식으로 진행함 => crawling 두번 진행

# 20230930에 대한 접속을 대한 코드 구성한후 9월 전체에 대해서 적용

import requests
from bs4 import BeautifulSoup
import re # 정규표현식 사용

response = requests.get("https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=001&date=20230930&page=1", headers={"User-agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")
# 현재 페이지 확인
page_find = soup.select_one(".paging")
page_text = str(page_find)
page_result = re.search("(?<=<strong>)[0-9]*", page_text)
page_result = page_result.group()
page_result = int(page_result)
print("현재 페이지: ", page_result)

# 기사제목
title_find = soup.select("dl > dt > a")
title = []
for i in title_find:
    title.append(i.text.strip())
title = list(filter(len, title))

# print("기사제목: ", title)

# 날짜
date_find = soup.select(".date")
date = []
for i in date_find:
    date.append(i.text)

# 날짜형식 맞추기(2023xxxx)
date_result = []
for i in date:
    date_result.append(i.split(".")[0] + i.split(".")[1] + i.split(".")[2])

# print("날짜: ", date_result)

# 기사본문, 반응 확인하기 위한 url크롤링
url_find = soup.select("dt > a")
url = []
for i in url_find:
    url.append(i.attrs["href"])

# url 중복 제거
url_result = []
for i in url:
    if i not in url_result:
        url_result.append(i)

# print("기사 url: ", url_result)

# 기사본문/기사반응
article_result = [] # 기사본문
# 검색된 기사 url에 대한 각각의 크롤링 후 기사본문/기사반응 수집
for article in url_result:
    article_response = requests.get(article, {"User-agent": "Mozilla/5.0"})
    article_soup = BeautifulSoup(article_response.text, "html.parser")

    # 기사본문
    text_find = article_soup.select("div > article") # 스포츠외의 기사
    sport_text = article_soup.select(".content_area > .news_end") # 스포츠기사
    like_result = [] # 기사반응
    if len(text_find) != 0:
        text_result = re.sub("[^0-9가-힣].[a-z0-9]+@[a-z0-9.]+.[(\[].*[)\]]", "", text_find[0].text.strip())
        text_result = re.sub("[^0-9가-힣].[a-z0-9]+@[a-z0-9.]*", "", text_result)
        # print(text_result)
        # print("=============================================================================================")
        article_result.append(text_result)
        like_find = article_soup.select(".u_likeit_list")
        for like in like_find:
            like_result.append(like)
    else:
        sport_result = re.sub("[^0-9가-힣].[a-z0-9]+@[a-z0-9.]+.[(\[].*[)\]]", "", sport_text[0].text.strip())
        sport_result = re.sub("[^0-9가-힣].[a-z0-9]+@[a-z0-9.]*", "", sport_result)
        sport_find = re.findall(".*\n(?=기사제공 연합뉴스)", sport_result)
        sport_result = sport_find[0]
        # print(sport_result)
        # print("=============================================================================================")
        article_result.append(sport_result)
        like_sport = article_soup.select(".u_likeit_list_button")
        for like in like_sport:
            like_result.append(like)
    # print(like_result) # 카테고리명은 알맞게 나오나 카테고리별 수치가 사이트의 수치와 관계없이 모두 0으로 나옴
print(article_result)

# csv 파일 작성
import csv

f = open("news.csv", "w", newline="", encoding="utf-8")
wr = csv.writer(f)
index = ["날짜", "타이틀", "기사본문"]
wr.writerow(index)
csv_value = []
for i in range(len(date_result)):
    temp = []
    temp.append(date_result[i])
    temp.append(title[i])
    temp.append(article_result[i])
    csv_value.append(temp)

for i in csv_value:
    wr.writerow(i)
f.close()