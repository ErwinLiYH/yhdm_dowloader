import requests
from bs4 import BeautifulSoup

# con = requests.get('http://www.yhdm.tv/v/3746-1.html')
# print(con.status_code)
# soup = BeautifulSoup(con.text,"html.parser")
# a = soup.find(name='div',id = 'playbox')
# dow_url = a['data-vid']
# print(dow_url)

con = requests.get('https://jx.youyitv.com/?url=1075_0b53dubr4aadqmalxzby4npdahiedyoqghsa')
print(con.status_code)

with open('a.html','wb') as b:
    b.write(con.content)