from bs4 import BeautifulSoup
import requests
import re

all_url = []
cnt = 0

url = 'https://ko.wikipedia.org/wiki/%ED%8C%8C%EC%9D%B4%EC%8D%AC'
r = requests.get(url)
html = r.text
soup = BeautifulSoup(html, "html.parser")

#전체 html에서 body만 추출
body = soup.find('body')

#태그명이 footer인 태그 존재 확인, 없다면 id명이 footer인 태그 존재확인 -> 제거
footer = body.find('footer')
if footer == None:
    foot = body.find('div', id="footer")
    foot.extract()
else:
    footer.extract()

#footer가 제거된 body부분에서 a태그 모두 찾기
a_tags = body.find_all("a")

#모든 a태그를 돌면서 링크가 존재하는 href속성 추출하기
for a_tag in a_tags:
    if "href" in str(a_tag):
        if "#" in str(a_tag) or "javascript:;" in str(a_tag) or "javascript::" in str(a_tag): #a태그 안에 링크가 존재하는지 확인
            continue
        else: #존재한다면 all_url리스트에 저장
            for new_href in all_url: #for문을 이용하여 리스트의 내용과 중복검사
                if new_href == a_tag["href"]:
                    cnt += 1
            if cnt == 0:
                all_url.append(a_tag["href"])
            cnt = 0
    else:
        continue
#리스트 내용 출력
print(all_url)



