# 네이버 뉴스 크롤링
# 20230831 ~ 20230801까지의 각 URL로 접속한 후 각 기사에 접속하는 방식으로 진행함 => crawling 두번 진행

# 20230831에 대한 접속을 대한 코드 구성한후 8월 전체에 대해서 적용

import requests
from bs4 import BeautifulSoup

response = requests.get("https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=001&date=20230831&page=1", headers={"User-agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")

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
print(url_find)