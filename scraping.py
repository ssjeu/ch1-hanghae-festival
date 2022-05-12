from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import certifi
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.uhugw.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.ch1

driver = webdriver.Chrome('./chromedriver')  # 드라이버를 실행합니다.
url = "https://korean.visitkorea.or.kr/list/fes_list.do?choiceTag=2022%EB%AC%B8%ED%99%94%EA%B4%80%EA%B4%91%EC%B6%95%EC%A0%9C&choiceTagId=0092f088-e6c9-425a-92f0-1bc474c43af7"

driver.get(url)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
sleep(1)  # 페이지가 로딩되는 동안 1초 간 기다립니다.

db.festivals.delete_many({})

for i in range(1, 10):
    try:
        driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/div[2]//*[@id="' + str(i) +'"]').send_keys(Keys.ENTER)
        #sleep(1)
        req = driver.page_source  # html 정보를 가져옵니다.

        soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱해줍니다.
        festivals = soup.select('#contents > div.wrap_contView.clfix > div.box_leftType1 > ul > li')

        for festival in festivals:
            name = festival.select_one('div.area_txt > div > a').text  # 앞에 공통적인 부분은 다 빼고 이름부분만 뽑기
            img_url = festival.select_one('div.photo > a > img')['src']
            real_date = festival.select_one('div.area_txt > p:nth-child(2)').text[1:17]
            date = festival.select_one('div.area_txt > p:nth-child(2)').text[6:8]


            festival_list = list(db.festivals.find({}, {'_id': False}))
            count = 0
            count = count + 1
            num = len(festival_list) + count

            print(num, name, img_url, real_date, date)

            doc = {
                'num': num,
                'name': name,
                'img_url': img_url,
                'real_date': real_date,
                'date': date,
                'like': 0
            }
            db.festivals.insert_one(doc)

    except NoSuchElementException:
        break

driver.quit()  # 정보를 가져왔으므로 드라이버는 꺼줍니다.

print(len(festival_list)+1)

#contents > div.wrap_contView.clfix > div.box_leftType1 > ul > li:nth-child(1) > div.area_txt > div > a
