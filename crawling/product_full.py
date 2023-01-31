import time
from requests import options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs

# 콘솔창 초기화
import os
os.system('cls') # window 

# 리스트 페이지
driver = webdriver.Chrome(executable_path="chromedriver_win32\chromedriver.exe")
listUrl = "http://www.thehandsome.com/ko/c/we051/#1_0_0_0_0_932_0_0_0"
driver.get(listUrl)

# for page in range(1, 648):
for page in range(1, 10):
    print("--" , driver.current_url)
    # listUrl = "http://www.thehandsome.com/ko/c/we#"+str(page)+"_0_0_0_0_7758_0_0_0"

    driver.get(driver.current_url)

    wait = WebDriverWait(driver, 10)
    element1 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'item_box')))
    listParse = bs(driver.page_source, 'html.parser')
    time.sleep(3)

    # 아이템 박스 리스트
    itemBox = listParse.select('#listBody > li > div')

    # 작업중~
    for i in range(0, 12):
        result = itemBox[i] 

        # p_common >> PID,PNAME,PNOTE,BNO,PSTATUS
        item_info = result.select_one('a.item_info2')
        # print(item_info)
        PID =  item_info.select_one('.price > span')['id'].split('_')[1]
        PNAME = item_info.select_one('.title').get_text()
        BNAME = item_info.select_one('.brand').get_text()
        # PSTATUS = item_info.select_one('.flag > span').get_text()
        print()
        print("insert into product_common (PID, PNAME, BNO) \nVALUES ('{0}', '{1}', (select BNO from brand where BNAME='{2}'));".format(PID, PNAME, BNAME))
        print("insert into product_category (cateno, pid) values (1, '{}');".format(PID)) # category

        # p_color >> PCID, PCIMG1,PCIMG2,PCIMG3,PCCHIPIMG, PCCOLORCODE,PCPRICE,PID,PRELEASEDATE
        colorInfo = result.select('.color_more_wrap > a')
        # print(colorInfo)

        imgInfo = result.select('#listBody > li > div > a > span.item_img > img')
        # print(imgInfo)
        PCIMG1src = (imgInfo[0].get('src')).split('_')
        PCIMG2src = (imgInfo[1].get('src')).split('_')
        PCIMG3 = 'http://cdn.thehandsome.com/_ui/desktop/common/images/products/no_img3.jpg' #로딩 실패

        for i in colorInfo :
            PCID = PID +'_'+ i['onclick'][-4:-2]
            # print(PCID)

            styletag = i['style']
            PCCOLORCODE = styletag[styletag.find('#'): styletag.find('#')+7]
            PCCHIPIMG = styletag[styletag.find("'")+1 : styletag.find("');")]
            # print('PCCOLORCODE:', PCCOLORCODE)
            # print('PCCHIPIMG: ', PCCHIPIMG)
            
            PCIMG1 = '_'.join([PCIMG1src[0], i['onclick'][-4:-2], PCIMG1src[2]])
            PCIMG2 = '_'.join([PCIMG2src[0], i['onclick'][-4:-2], PCIMG2src[2]])
            # print(PCIMG1)
            # print(PCIMG2)

            # print(PCPRICE)
            PCPRICE = (item_info.select_one('.price > span > span')).get_text().replace('￦', '').replace(',', '')
            print("insert into product_color (PCID, PCIMG1, PCIMG2, PCIMG3, PCCHIPIMG, PCCOLORCODE, PCPRICE, PID) \nvalues('{}', \n'{}', \n'{}', \n'{}', \n'{}', '{}', {}, '{}');".format(PCID, PCIMG1,PCIMG2,PCIMG3,PCCHIPIMG, PCCOLORCODE,PCPRICE,PID))
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