from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
from yarl import URL
from keyword_function import option1

data_list = []
all_url = []
cnt = 1

def issame(url):
    # 중복검사
    count = 0
    if url in all_url:
        count += 1
    if count == 0:
        store(url)

def store(url):
    global cnt
    all_url.append(url)
    # 재웅 + 대규 코드 (데이터 저장, 결과 만들기)
    data_list = option1(url, Keyword)
    if len(data_list) != 0: # 출력이 된다는 건 keyword_function함수로 인한 리턴된 리스트 값이 있단 뜻
        print(cnt)
        cnt += 1
        allList(url)

def allList(url):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    yarl_url = URL(url)
    base_url = yarl_url.scheme + "://" + yarl_url.host
    # yarl_url.scheme : URL의 스키마(http or https), yarl_url.host : URL의 도메인주소

    try: # requests.get(url, verity=false)로 response 확인 필요함
        r = requests.get(url, verify=False)
        if cnt == 1: #처음 URL의 데이터도 저장해야 하기 때문
            all_url.append(url) #처음 URL도 all_url에 저장해야 함
            # 재웅 + 대규 코드 (데이터 저장)
            #Text_Ranking.main(url, Keyword)

        ## 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시
        soup = BeautifulSoup(r.text, "lxml")

        # 전체 html에서 body의 a태그 모두 찾기
        a_tags = soup.find('body').findAll("a")

        # 모든 a태그를 돌면서 링크가 존재하는 href속성 추출하기
        for a_tag in a_tags:
            if "href" in str(a_tag):  # a태그 안에 href속성이 존재하는지 확인
                if a_tag["href"].startswith("http"):  # 정상적인 url형식인지 확인
                    ch_url = a_tag["href"]
                else:  # http://가 없는 href들
                    if a_tag["href"].startswith("#") or a_tag["href"].startswith("javascript:"):  # 공통적으로 필요없는 href들 제거
                        continue
                    else:  # http~가 없는 url에 base_url을 결합
                        if a_tag["href"].startswith("/"):
                            ch_url = base_url + a_tag["href"]
                        else:
                            ch_url = base_url + "/" + a_tag["href"]
                issame(ch_url)
            else:
                continue
    except:
        pass

Url = input("URL을 입력하세요 : ")
Keyword = input("아니 시발 도대체 무슨 키워드를 알고싶은건데?? : ")
allList(Url)
print(data_list)
