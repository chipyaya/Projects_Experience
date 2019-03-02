# env = python3

from bs4 import BeautifulSoup
import requests
import time
import re
import pickle

def get_webpage(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def get_articles(webpage):
    soup = BeautifulSoup(webpage, 'html.parser')

    articles = []
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('a'):  # 有超連結，表示文章存在
            href = d.find('a')['href']
            title = d.find('a').text
            if '食記' in title:
                articles.append({
                    'isSponsoredPost': False,
                    'title': title,
                    'href': href,
                })
            elif '廣宣' in title:
                articles.append({
                    'isSponsoredPost': True,
                    'title': title,
                    'href': href,
                })
    return articles

def get_content(webpage):
    soup = BeautifulSoup(webpage, 'html.parser')
    main_content = soup.find(id='main-content')

    # 移除標頭
    for meta in main_content.find_all('div','article-metaline'):
        meta.extract()
    for meta in main_content.find_all('div','article-metaline-right'):
        meta.extract()
    # 移除連結
    for a in main_content.find_all('a'):
        a.extract()

    pushes = main_content.find_all('div', 'push')
    push_contents = []
    for push in pushes:
        push.extract()
        push_content = push.find('span', 'push-content').text[2:] # 移除 ': '
        push_contents.append(push_content)

    strings = main_content.strings
    content = ''
    for s in strings:
        # 移除 '※ 發信站:', '※ 文章網址:'與空行
        if s[0] in '※' or not s.strip():
            continue
        content += s
    return push_contents, content

def main():

    ptt_url = 'https://www.ptt.cc'
    food_url = 'https://www.ptt.cc/bbs/Food/index'
    page_index = 6000 # Need to be assign
    count = 0
    max_count = 50000 # Need to be assign
    while True:
        url = food_url + str(page_index) + '.html'
        webpage = get_webpage(url)
        articles = get_articles(webpage)
        for article in articles:
            if count > max_count:
                return 0 # Ends the program
            webpage = get_webpage(ptt_url + article['href'])
            article['push_contents'], article['content'] = get_content(webpage)
            filename = 'ptt_posts/' + str(count) + '.p'
            pickle.dump(article, open(filename, 'wb'))
            count += 1
        page_index -= 1

if __name__ == '__main__':
    main()
