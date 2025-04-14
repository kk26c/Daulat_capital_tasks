import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

sources = {
    'Moneycontrol IT': 'https://www.moneycontrol.com/news/business/technology/',
    'Economic Times IT': 'https://economictimes.indiatimes.com/tech',
    'Infosys Reports': 'https://www.infosys.com/investors/reports-filings/quarterly-results.html'
}

def scrape_moneycontrol(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = soup.find_all('li', class_='clearfix')
    data = []

    for article in articles[:10]:
        headline = article.find('h2')
        if headline:
            title = headline.get_text(strip=True)
            link = headline.a['href'] if headline.a else None
            date = datetime.today().strftime('%Y-%m-%d')
            data.append({'Source': 'Moneycontrol IT', 'Title': title, 'Link': link, 'Date': date})
    return data


def scrape_infosys_reports(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    data = []

    for link in soup.find_all('a', href=True):
        if 'pdf' in link['href'].lower():
            title = link.get_text(strip=True)
            href = 'https://www.infosys.com' + link['href']
            date = datetime.today().strftime('%Y-%m-%d')  # Placeholder date
            data.append({'Source': 'Infosys Reports', 'Title': title, 'Link': href, 'Date': date})
    return data

all_data = []


all_data.extend(scrape_moneycontrol(sources['Moneycontrol IT']))


all_data.extend(scrape_infosys_reports(sources['Infosys Reports']))


df = pd.DataFrame(all_data)


df.to_csv('financial_updates.csv', index=False)
print("Data saved to financial_updates.csv")
