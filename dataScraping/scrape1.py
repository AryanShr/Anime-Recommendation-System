import requests
from bs4 import BeautifulSoup
import csv
import time
import logging

# Set up logging
logging.basicConfig(filename='scraping1.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

# Function to scrape anime data
def scrape_anime_data(url):
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, 'html.parser')
        anime = soup.select('table.top-ranking-table tr.ranking-list')

        for item in anime:
            # Extract data
            link = item.select_one('td.title div.detail div.di-ib.clearfix h3 a')['href'] + "/stats"
            id = link.split('/')[4]
            subres = requests.get(link, headers=headers)
            subsoup = BeautifulSoup(subres.content, 'html.parser')
            genre = [cat.text for cat in subsoup.select('[itemprop*="genre"]')]
            rank = item.select_one('td.rank span').text
            title = item.select_one('td.title div.detail div.di-ib.clearfix h3 a').text.encode('utf-8')
            score = item.select_one('td.score span.score-label').text
            info = item.select_one('div.detail div.information.di-ib.mt4').text.split('\n')
            episodes = info[1].strip().split(' ')[1][1:]
            status = info[2].strip().split(' ')
            members = info[3].strip().split(' ')[0]
            rating = {10: 0, 9: 0, 8: 0, 7: 0, 6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
            
            for j in range(1, 11):
                rating[j] = int(subsoup.find('td', class_=f"score-label score-{j}").parent.select_one('td div.spaceit_pad span small').text[1:-7])
            
            val = {'id': id, 'rank': rank, 'title': title, 'score': score, 'genre': genre, 'episodes': episodes, 'members': members, 'rating': rating}
            writer.writerow(val)
            print(val)
        
        return True
    except Exception as e:
        logging.error(str(e))
        return False

# Retry function with exponential backoff
def retry(func, url):
    max_attempts = 5
    wait_time = 2  # initial wait time in seconds

    for attempt in range(max_attempts):
        try:
            if func(url):
                return True
        except Exception as e:
            logging.error(str(e))
            continue
        # Wait before retrying
        time.sleep(wait_time)
        wait_time *= 2  # exponential backoff

    return False

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
}

with open('animeDB2.csv', 'a+', newline='') as csvfile:
    fieldnames = ['id', 'rank', 'title', 'score', 'genre', 'episodes', 'members', 'rating']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Check if the file is empty
    csvfile.seek(0)
    if not csvfile.read(1):
        writer.writeheader()
    # count line in csv file
    cnt = 0
    csvfile.seek(0)
    for line in csvfile:
        cnt += 1
    print(cnt)
    for i in range(cnt-1+5001, 10001, 50):
        url = 'https://myanimelist.net/topanime.php?limit=' + str(i)

        if retry(scrape_anime_data, url):
            csvfile.flush()  # Flush the buffer to ensure data is written to the file
            continue
        else:
            logging.error(f"Failed to scrape data from {url}")
            break  # Exit the loop to avoid overwriting the file on the next run
