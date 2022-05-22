import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time
import re

def text_to_word(text):
    pattern= ";|,|\n|\.|\?|\!|\s+"
    preview = text.lower()
    preview = re.split(pattern, preview)
    return set(preview)

url='https://habr.com/ru/all'  # без этого не делает выдачу контента
url1='https://habr.com' # без этого кривые ссылки
DESIRED_HUBS = ['дизайн', 'фото', 'web', 'python','it-эмиграция','базовые' , 'bpmn']

interval = input('Введите интервал проверки (сек):' )
session = HTMLSession()
response = session.get(url)
text = response.text # голый текст страницы
soup = BeautifulSoup(text, features='html.parser')  # features='lxml')

not_war = True
while not_war:
    articles = soup.find_all('article')  # список объектов article выдает find_all -
    for article in articles:
        hubs = article.find_all(class_="tm-article-snippet__hubs-item")
        # class="article-formatted-body article-formatted-body article-formatted-body_version-1" version меняются 1 2
        preview1 = article.find(class_="article-formatted-body article-formatted-body article-formatted-body_version-1")
        preview2 = article.find(class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
        if preview1:
            preview = preview1
        elif preview2:
            preview = preview2
        else:
            print('что то пошло не так')
        preview = text_to_word(preview.text)
        hubs = set(hub.text.strip() for hub in hubs) # set избавляемся от дублей  strip избавляемся от пробелов
        href = article.find(class_="tm-article-snippet__title-link").attrs['href']
        date = article.find('time').attrs['title']
        date1 = article.find('time').text
        link = url1 + href
        title = head = article.find(class_='tm-article-snippet__title-link').text
        # или так
        title = article.find('h2').find('span').text  # контейнер h2 статьи и в нем найти span
        title_set = text_to_word(title)

        DESIRED_HUBS  = set(DESIRED_HUBS)
        intersection = preview.intersection(DESIRED_HUBS)
        intersection2 = title_set.intersection(DESIRED_HUBS)

        for hub in hubs:
            if hub.lower() in DESIRED_HUBS or intersection or intersection2:
                result= f'{date}, {date1}, Статья - {title} доступна по ссылке- {link}'
                print(result)
                # новый запрос
                response = requests.get(link) #, headers=HEADERS)#)  конкретная статья
                break
    time.sleep(int(interval))
