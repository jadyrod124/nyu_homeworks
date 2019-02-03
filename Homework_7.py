import requests
import jinja2
import urllib.request
from bs4 import BeautifulSoup

url = 'https://www.nytimes.com/2017/10/29/business/virtual-reality-driverless-cars.html'

def scrape_times_article(url):
    response = requests.get(url)
    pg_text = response.text
    soup = BeautifulSoup(pg_text, 'html.parser')

    title = soup.find('title').text
    byline = soup.find('span', {'class': 'css-1baulvz'}).text

    dateline = soup.find('time').text


    paragraph = soup.find_all('div', {'class': 'css-4w7y5l'})

    pars = [par.text for par in paragraph]

    env = jinja2.Environment()
    env.loader = jinja2.FileSystemLoader('./')
    template = env.get_template('story_template.html')
    completed_page = template.render(title=title, author=byline, date=dateline, paragraphs=pars)

scrape_times_article(url)
