from bs4 import BeautifulSoup
import requests

all_url = []
cnt = 0

base_url = "https://www.crummy.com"
url = 'https://www.crummy.com/software/BeautifulSoup/bs4/doc/#'
r = requests.get(url)
html = r.text
soup = BeautifulSoup(html, "lxml")

#전체 html에서 body만 추출
body = soup.find('body')

#태그명이 footer인 태그 존재 확인, 없다면 id명이 footer인 태그 존재확인 -> 제거
# footer = body.find('footer')
# if footer == None:
#     foot = body.find('div', id="footer")
#     foot.extract()
# else:
#     footer.extract()

#footer가 제거된 body부분에서 a태그 모두 찾기
a_tags = body.find_all("a")

#모든 a태그를 돌면서 링크가 존재하는 href속성 추출하기
for a_tag in a_tags:
    if "href" in str(a_tag): #a태그 안에 링크가 존재하는지 확인
        if "http" in a_tag["href"][0:5]: #정상적인 url형식인지 확인
            for new_href in all_url: #for문을 이용하여 리스트의 내용과 중복검사
                if new_href == a_tag["href"]:
                    cnt += 1
            if cnt == 0:
                res = requests.get(a_tag["href"])
                if res.status_code == 404:
                    continue
                all_url.append(a_tag["href"]) #정상접근이 가능한 URL 저장
        else: #http://가 없는 href들
            if "#" in a_tag["href"][0:1] or "javascript:" in a_tag["href"]: #공통적으로 필요없는 href들 제거
                continue
            else:
                if "/" not in a_tag["href"][0:1]:
                    ch_url = base_url + "/" + a_tag["href"]
                else:
                    ch_url = base_url + a_tag["href"] #http~가 없는 url에 base_url을 결합
                for new_href in all_url:  # for문을 이용하여 리스트의 내용과 중복검사
                    if new_href == ch_url:
                        cnt += 1
                if cnt == 0: #중복이 없는 경우
                    res = requests.get(ch_url)
                    if res.status_code == 404:
                        continue
                    all_url.append(ch_url) #정상 접근이 가능한 URL 저장
        cnt = 0
    else:
        continue
#리스트 내용 출력
print(len(all_url))
