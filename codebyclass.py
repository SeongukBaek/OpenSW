from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
from yarl import URL

all_url = []
now_deep = 1 # 현재의 deep 값
fin = 0

class Href(object):
    def __init__(self, url, how_deep, Keyword, option):
        self.url = url
        self.how_deep = how_deep
        self.Keyword = Keyword
        self.option = option
        self.issame(self.url)

    def issame(self, url): # 중복검사
        global now_deep
        global fin
        count = 0
        if url in all_url:
            count += 1
        if count == 0:
            all_url.append(url)
            # 재웅 + 대규 코드 (데이터 저장, 결과 만들기)
            # 데이터 저장한 url에 대해서 allList(url)
            if fin == 0:
                now_deep += 1
                if now_deep < self.how_deep:
                    All(self.url, self.how_deep, self.Keyword, self.option)
                if now_deep == self.how_deep:
                    fin = 1  # fin = 1 -> 원하는 깊이까지 도달

class All(object):
    def __init__(self, url, how_deep, Keyword, option):
        self.url = url
        self.how_deep = how_deep
        self.Keyword = Keyword
        self.option = option
        self.allList(self.url)

    def allList(self, url):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        yarl_url = URL(url)
        base_url = yarl_url.scheme + "://" + yarl_url.host
        # yarl_url.scheme : URL의 스키마(http or https), yarl_url.host : URL의 도메인주소

        try: # requests.get(url, verity=false)로 response 확인 필요함
            r = requests.get(url, verify=False)
            if now_deep == self.how_deep: # 사용자가 입력한 깊이와 시작 깊이가 같을 경우 -> 사용자가 1을 입력한 경우
                all_url.append(url)
                # 재웅 + 대규 코드 (true면 데이터 저장)
                pass # 더이상 탐색하지 않고 종료
            else:
                if now_deep == 1: #처음 URL의 데이터도 저장해야 하기 때문
                    all_url.append(url) #처음 URL도 all_url에 저장해야 함
                    # 재웅 + 대규 코드 (true면 데이터 저장)

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
                        Href(ch_url, self.how_deep, self.Keyword, self.option)
                    else:
                        continue
        except:
            pass

def execute(Url, how_deep, Keyword, option):
    All(Url, how_deep, Keyword, option)
