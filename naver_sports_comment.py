import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

for date in range(20, 30):
    index = 1
    pageindex = 0
    while True:
        url = 'https://sports.news.naver.com/wfootball/news/index.nhn?&isphoto=N&type=comment' + '&page=' + str(
            index) + '&date=202007' + str(date)
        driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
        driver.implicitly_wait(30)
        # raw = requests.get(url)
        #
        # html = BeautifulSoup(raw.text, "html.parser")
        driver.get(url)
        pageindex = driver.find_element_by_css_selector('#_pageList')
        pagelen = len(pageindex.text.replace(" ", ""))
        news = driver.find_elements_by_css_selector('#_newsList div.text a.title')
        for n in range(0, len(news)):
            news[n] = news[n].get_attribute("href")
        for n in range(0, len(news)):
            article_url = news[n]
            driver.get(article_url)
            all = driver.find_element_by_css_selector('a.u_cbox_btn_view_comment')
            all.click()
            while True:
               try:
                   more = driver.find_element_by_css_selector('a.u_cbox_btn_more')
                   more.click()
                   time.sleep(1)
               except:
                    break

            contents = driver.find_elements_by_css_selector('span.u_cbox_contents')
            for content in contents:
                print(content.text)
        driver.quit()
        index += 1
        if index > pagelen:
            index = 1
            break
