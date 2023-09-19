# 네이버 뉴스 크롤링
# 20230831 ~ 20230801까지의 각 URL로 접속한 후 각 기사에 접속하는 방식으로 진행함 => crawling 두번 진행

# 20230831에 대한 접속을 대한 코드 구성한후 8월 전체에 대해서 적용

import requests
from bs4 import BeautifulSoup
import re # 정규표현식 사용

response = requests.get("https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=001&date=20230831&page=1", headers={"User-agent": "Mozilla/5.0"})
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
# 검색된 기사 url에 대한 각각의 크롤링 후 기사본문/기사반응 수집
for article in url_result:
    article_response = requests.get(article, {"User-agent": "Mozilla/5.0"})
    article_soup = BeautifulSoup(article_response.text, "html.parser")

    # 기사본문
    text_find = article_soup.select("div > article") # 스포츠외의 기사
    sport_text = article_soup.select(".content_area > .news_end")
    
    for text in sport_text:
        # print(text.text.strip())
        text_result = re.sub("[^0-9가-힣].[a-z0-9]+@[a-z0-9.]+.[(\[].*[)\]]", "", text.text.strip())
        text_result = re.sub("[^0-9가-힣].[a-z0-9]+@[a-z0-9.]*", "", text_result)
        text_find = re.findall(".*\n(?=기사제공 연합뉴스)", text_result)
        print(text_find)
        print("============================================================================================================")