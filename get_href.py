from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
all_url = []
cnt = 0
base_url = "http://medium.com"
url = 'https://medium.com/@keyhyuk.kim/python-%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%9F%AC-%EB%8F%84%EA%B5%AC-%EB%B9%84%EA%B5%90-%EB%B0%8F-%EC%82%AC%EC%9A%A9-%ED%9B%84%EA%B8%B0-scrapy-vs-selenium-vs-requests-urllib-6483041ca1ba'

r = requests.get(url)
## 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시
soup = BeautifulSoup(r.text, "lxml")

def extract_foot(body):
    #태그명이 footer인 태그 존재 확인, 없다면 id명이 footer인 태그 존재확인 -> 제거
    footer = body.find('footer')
    if footer == None:
        foot = body.find('div', id="footer")
        foot.extract()
    else:
        footer.extract()
    #태그명, id명이 footer인 태그를 모두 제거한 body를 return
    return body

def issame(url):
    # for문을 이용하여 리스트의 내용과 중복검사
    count = 0
    for new_href in all_url:
        if new_href == url:
            count += 1
    return count

def isvalid_store(url):
    #해당 URL이 유효한지 확인, 유효하다면 all_url 리스트에 저장
    try:
        requests.get(url, verify=False)
        all_url.append(url)
    except:
        pass

#전체 html에서 body만 추출
body = soup.find('body')

#태그명이 footer인 태그 존재 확인, 없다면 id명이 footer인 태그 존재확인 -> 제거
# body = extract_foot(body)

#footer가 제거된 body부분에서 a태그 모두 찾기
a_tags = body.find_all("a")

#모든 a태그를 돌면서 링크가 존재하는 href속성 추출하기
for a_tag in a_tags:
    if "href" in str(a_tag): #a태그 안에 href속성이 존재하는지 확인
        if "http" in a_tag["href"][0:5]: #정상적인 url형식인지 확인
            cnt = issame(a_tag["href"])
            if cnt == 0:
                isvalid_store(a_tag["href"])
        else: #http://가 없는 href들
            if "#" in a_tag["href"][0:1] or "javascript:" in a_tag["href"]: #공통적으로 필요없는 href들 제거
                continue
            else:
                if "/" not in a_tag["href"][0:1]:
                    ch_url = base_url + "/" + a_tag["href"]
                else:
                    ch_url = base_url + a_tag["href"] #http~가 없는 url에 base_url을 결합
                cnt = issame(ch_url)
                if cnt == 0: #중복이 없는 경우
                    isvalid_store(ch_url)
        cnt = 0
    else:
        continue
#리스트 내용 출력
print(all_url)
