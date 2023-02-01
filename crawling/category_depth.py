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
    print(i, ")", cateString)
    depth1.add(cateString[0])
    depth2.add(cateString[1])
    depth3.add(cateString[2])

print("-- depth1")
for d1 in depth1:
    print("insert into depth1 (depth1name) VALUES ('{0}');".format(d1))

print("\n-- depth2")
for d2 in depth2:
    print("insert into depth2 (depth2name) VALUES ('{0}');".format(d2))

print("\n-- depth3")
for d3 in depth3:
    print("insert into depth3 (depth3name) VALUES ('{0}');".format(d3))

# print(depth1)
# print(depth2)
# print(depth3)


