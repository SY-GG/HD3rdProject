import requests
from bs4 import BeautifulSoup as bs


import os
os.system('cls') # window 


page = requests.get("http://www.thehandsome.com/ko/");
soup = bs(page.text, "html.parser");

elements = soup.select('#cate_m_main > li > div > div > ul > li > ul > li > a')

depth1 = set([])
depth2 = set([])
depth3 = set([])

for i in range(42,176):
    cateString = elements[i]["onclick"].split(',')[2][1:-3].split('_')
    print("INSERT INTO CATEGORY (CATENO, DEPTH1NAME, DEPTH2NAME, DEPTH3NAME) VALUES (category_seq.NEXTVAL, '{}', '{}', '{}');".format(cateString[0], cateString[1], cateString[2]))