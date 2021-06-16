import urllib.request
from bs4 import BeautifulSoup

f = open("test.txt","w",encoding="utf-8")
h = {'User-Agent':'Mozilla/5.0'}
url = "https://www.melon.com/chart/index.htm"
req = urllib.request.Request(url,headers=h)
a = urllib.request.urlopen(req)
b = a.read().decode('utf-8') 
soup = BeautifulSoup(b,'html.parser')
c = soup.find_all(class_="rank01")
i = 1
for n in c:
    f.write(str(i)+" : "+str(n.get_text().strip()+"\n"))
    i = i + 1
f.close()