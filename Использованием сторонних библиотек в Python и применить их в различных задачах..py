"""
pip install requests — для отправки HTTP-запросов.
pip install beautifulsoup (из пакета beautifulsoup4) — для парсинга HTML-контента
pip install lxml  Опционально

Как работает этот код:
1. Получает главную страницу: Код отправляет GET-запрос к главной странице сайта.
2. Парсит главную страницу: Использует BeautifulSoup для извлечения заголовков и ссылок на статьи.
3. Запрашивает каждую статью: По каждой найденной ссылке выполняется GET-запрос, чтобы получить полное описание статьи.
4. Извлекает описание: На каждой странице статьи ищется метатег <meta name="description">, и извлекается его содержимое.
5. Выводит результаты: Название и описание каждой статьи выводятся в консоль.

На примере сайта: https://chessfond.ru/

"""

import requests
from bs4 import BeautifulSoup
# Выполняем GET-запрос к главной странице сайта
response = requests.get('https://chessfond.ru')
if response.status_code == 200:
    print("Успешный GET-запрос к главной странице!\n")
    # Используем BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # Замените селектор на актуальный для вашего сайта
    posts = soup.find_all('article', limit=10)  # Замените 'article' на актуальный тег для постов
    # Обходим найденные посты и выводим названия и описания
    for post in posts:
        # Получаем заголовок и ссылку на статью
        title = post.find('h2').text.strip() if post.find('h2') else 'Без названия'  # Замените 'h2' на актуальный селектор для названия
        link = post.find('a')['href'] if post.find('a') else None  # Предполагается, что ссылка на статью находится внутри тега <a>
        if link:
            # Выполняем GET-запрос к странице статьи
            article_response = requests.get(link)
            if article_response.status_code == 200:
                # Используем BeautifulSoup для парсинга HTML страницы статьи
                article_soup = BeautifulSoup(article_response.text, 'html.parser')
                # Получаем описание из meta description
                description_meta = article_soup.find('meta', attrs={'name': 'description'})
                description = description_meta['content'] if description_meta else 'Без описания'
                print(f'Название: {title}\nОписание: {description}\n')
            else:
                print(f"Ошибка при получении данных статьи по ссылке {link}: {article_response.status_code}")
else:
    print("Ошибка при получении данных главной страницы:", response.status_code)