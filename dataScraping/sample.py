import requests
from bs4 import BeautifulSoup

url = 'https://myanimelist.net/topanime.php?limit=0'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
}
res = requests.get(url,headers=headers)
status,txt = res.status_code, res.text
soup = BeautifulSoup(res.content, 'html.parser')
anime = soup.select('table.top-ranking-table tr.ranking-list')
for item in anime:
    link = item.select_one('td.title div.detail div.di-ib.clearfix h3 a')['href']+"/stats"
    id = link.split('/')[4]
    subres = requests.get(link,headers=headers)
    subsoup = BeautifulSoup(subres.content, 'html.parser')
    genre = [cat.text for cat in subsoup.select('[itemprop*="genre"]')]
    rank = item.select_one('td.rank span').text
    title = item.select_one('td.title div.detail div.di-ib.clearfix h3 a').text.encode('utf-8')
    score = item.select_one('td.score span.score-label').text
    info = item.select_one('div.detail div.information.di-ib.mt4').text.split('\n')
    episodes = info[1].strip().split(' ')[1][1:]
    status = info[2].strip().split(' ')
    members = info[3].strip().split(' ')[0]
    rating = {10:0,9:0,8:0,7:0,6:0,5:0,4:0,3:0,2:0,1:0}
    for i in range(1,11):
        rating[i] = int(subsoup.find('td', class_=f"score-label score-{i}").parent.select_one('td div.spaceit_pad span small').text[1:-7])
    print(id,rank, title, score,genre, episodes,members,rating)