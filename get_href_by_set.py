from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
from collections import deque
from yarl import URL

all_url = deque([])

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

# def issame(url):
#     # for문을 이용하여 리스트의 내용과 중복검사
#     count = 0
#     for new_href in all_url:
#         if new_href == url:
#             count += 1
#     if count == 0:
#         isvalid_store(url)

def isvalid_store(url):
    #해당 URL이 유효한지 확인, 유효하다면 all_url 리스트에 저장
    try:
        requests.get(url, verify=False)
        all_url.append(url)
    except:
        pass

def allList(url):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    yarl_url = URL(url)
    base_url = yarl_url.scheme + "://" + yarl_url.host
    # yarl_url.scheme : URL의 스키마(http or https), yarl_url.host : URL의 도메인주소

    r = requests.get(url)
    ## 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시
    soup = BeautifulSoup(r.text, "lxml")

    # 전체 html에서 body의 a태그 모두 찾기
    a_tags = soup.find('body').findAll("a")

    # 태그명이 footer인 태그 존재 확인, 없다면 id명이 footer인 태그 존재확인 -> 제거
    # body = extract_foot(body)

    # 모든 a태그를 돌면서 링크가 존재하는 href속성 추출하기
    for a_tag in a_tags:
        if "href" in str(a_tag): #a태그 안에 href속성이 존재하는지 확인
            if a_tag["href"].startswith("http"): #정상적인 url형식인지 확인
                isvalid_store(a_tag["href"])
            else: #http://가 없는 href들
                if a_tag["href"].startswith("#") or a_tag["href"].startswith("javascript:"): #공통적으로 필요없는 href들 제거
                    continue
                else:   #http~가 없는 url에 base_url을 결합
                    if a_tag["href"].startswith("/"):
                        ch_url = base_url + a_tag["href"]
                    else:
                        ch_url = base_url + "/" + a_tag["href"]
                    isvalid_store(ch_url)
        else:
            continue
    #리스트 반환
    my_set = set(all_url)
    return my_set

allList("https://ko.wikipedia.org/wiki/%EB%8C%80%EC%99%95%ED%8C%90%EB%8B%A4")
