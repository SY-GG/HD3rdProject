import time
from requests import options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs

import product_detail as detail

# 콘솔창 초기화
import os
os.system('cls') # window 

# 리스트 페이지
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# browser = webdriver.Chrome(options=options)
driver = webdriver.Chrome(executable_path="chromedriver_win32\chromedriver.exe", options=options)

listUrl = "http://www.thehandsome.com/ko/c/we101/#1_0_0_0_0_829_0_0_0"
driver.get(listUrl)

# FEAT: 카테고리 찾기
cateString= driver.current_url.split('/')[5]
depth1 = cateString[0:2]
depth2 = cateString[2:4]
depth3 = cateString[4:]
# print("{} : {}>{}>{}".format(cateString, depth1, depth2, depth3));


# FEAT: 전체 페이지 긁기
# FIXME: range 바꾸기
# for page in range(1, 2):
for page in range(1,5):
    print("--" , driver.current_url)
    pageUrl = driver.current_url
    wait = WebDriverWait(driver, 5)
    element1 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'item_box')))
    listParse = bs(driver.page_source, 'html.parser')
    time.sleep(3)

    itemBox = listParse.select('#listBody > li > div')

    #  FIXME: range 바꾸기
    for i in range(0, 12):
    # for i in range(3, 4):
        result = itemBox[i] 

        # NOTE: p_common >> PID,PNAME,PNOTE,BNO,PSTATUS
        item_info = result.select_one('a.item_info2')
        PID =  item_info.select_one('.price > span')['id'].split('_')[1]
        PNAME = item_info.select_one('.title').get_text()
        BNAME = item_info.select_one('.brand').get_text().replace("'", "''").replace("&", "\&")
        
        # FEAT: product_common 등록 후, category에 product 등록
        print("insert into product_common (PID, PNAME, BNO) VALUES ('{0}', '{1}', (select BNO from brand where BNAME='{2}'));".format(PID, PNAME, BNAME))
        print("insert into product_category (cateno, pid) values ((select cateno from CATEGORY where depth1name = '{}' and depth2name = '{}' and depth3name = '{}'), '{}');"
                .format(depth1, depth2, depth3, PID))

        wait = WebDriverWait(driver, 10)
        element1 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'adaptive_wrap')))
        itemParse = bs(driver.page_source, 'html.parser')
        # print(itemParse)

        colorInfo = result.select('.color_more_wrap > a')

        for i in colorInfo :
            colorName = i['onclick'][-4:-2]
            PCID = PID +'_'+ colorName
            # print(PCID)
            detail.getDetailInfo(PCID)

        print()

    time.sleep(1)
    xpath_button='//*[@id="bodyWrap"]/div[2]/div[2]/a[3]'
    driver.find_element(By.XPATH, xpath_button).click()
    time.sleep(2)

        




    # #아이템 상세
    # itemUrl = 'https://www.thehandsome.com/ko/HANDSOME/WOMEN/PANTS/DENIM/p/{}'.format(PID)
    # driver.get(itemUrl)

    # # 로딩 대기
    # wait = WebDriverWait(driver, 10)
    # element2 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'adaptive_wrap')))
    # itemParse = bs(driver.page_source, 'html.parser')