import json
import urllib.request as req

from bs4 import BeautifulSoup as bs

# 콘솔창 초기화
import os
os.system('cls')  # window


# 상세 페이지
def getDetailInfo(PCID):
    url = "http://www.thehandsome.com/ko/product/reloadProdSize?productcode=" + PCID
    res = req.urlopen(url)
    itemInfo = json.load(res)
    # print(itemInfo)

    # FEAT: product_color 테이블 추가
    PCIMG1 = itemInfo['product']['productImages'][0]['image']['url']
    PCIMG2 = itemInfo['product']['productImages'][1]['image']['url']
    PCIMG3 = itemInfo['product']['productImages'][2]['image']['url']

    # print(PCIMG1)
    # print(PCIMG2)
    # print(PCIMG3)

    PCCHIPIMG = itemInfo['product']['productImages'][3]['image']['url']
    # print(PCCHIPIMG)

    PCCOLORCODE = itemInfo['product']['variantOptions'][0]['rgbcode']
    # print(PCCOLORCODE)

    PCPRICE = int(itemInfo['product']['variantOptions']
                  [0]['priceData']['value'])
    PID = itemInfo['product']['baseProduct']
    # print(PCPRICE)
    # print(PID)

    # FEAT: PNOTE 수정
    PNOTE = itemInfo['product']['newDescription01']
    print("update product_common set PNOTE = '{}' where pid='{}';".format(PNOTE, PID).strip())

    # FEAT: product_color 삽입문
    print("insert into product_color (PCID, PCIMG1, PCIMG2, PCIMG3, PCCHIPIMG, PCCOLORCODE, PCPRICE, PID)")
    print("values('{}', '{}', '{}', '{}', '{}', '{}', {}, '{}');"
          .format(PCID, PCIMG1, PCIMG2, PCIMG3, PCCHIPIMG, PCCOLORCODE, PCPRICE, PID))

    # TODO: PRODUCT_STOCK
    for item in itemInfo['product']['variantOptions']:
        # NOTE: PSIZE 구하기
        defaultsize = item['variantOptionQualifiers'][2]['value']
        koreasize = item['koreaSize']
        PSIZE = '{}({})'.format(
            defaultsize, koreasize) if koreasize else defaultsize
        # print(PSIZE)

        print("insert into PRODUCT_STOCK (PSID, PSSTOCK, PSIZE, PCID) values ('{0}_{1}', 100, '{2}', '{0}');"
              .format(PCID, defaultsize, PSIZE).strip())

    print("-- 상세이미지")
    for idx, imginfo in enumerate(itemInfo['product']['productImages'][4:11]):
        IMGSRC = imginfo['image']['url']
        print("insert into PRODUCT_IMG(IMGSRC, PCID) VALUES('{}','{}');".format(IMGSRC, PCID))

    return getDetailInfo


getDetailInfo('OB2C9WJC037W_LE')
# getDetailInfo('LB2C8ABZ721U_LE')
