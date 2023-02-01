import requests
from bs4 import BeautifulSoup as bs

page = requests.get("http://www.thehandsome.com/ko/");
soup = bs(page.text, "html.parser");

elements = soup.select('#cate_m_main > li > div > div > ul > li > ul > li > a')

for element in elements:
    brandName = element.get_text()
    brandCode = element["href"].split("/")[-1][-2:]
    # if type(int(brandCode)) == int :
    print("insert into BRAND (BNO, BNAME) VALUES ({0}, '{1}');".format(brandCode, brandName))