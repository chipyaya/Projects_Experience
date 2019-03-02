from bs4 import BeautifulSoup
from os import listdir
import requests
import random
import pickle
import time


def get_bloglist():
    r = requests.get('https://blogranking.events.pixnet.net', params={'sort': 'populous', 'category': '14'})
    soup = BeautifulSoup(r.text, 'html.parser')
    bloglist = list()
    for x in soup.find_all('a', {'class': 'blogger-name'}):
        bloglist.append(x.get('href'))
    return bloglist


def get_post(url):
    i = 1
    while True:
        r = requests.get(f'{url}/listall/{i}')
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        postlist = list()
        for x in soup.find(id='article-area').find_all('a'):
            link = x.get('href')
            print(link, x.get_text())
            get_postcontent(link)
            if 'post' in link:
                postlist.append(link)
        if len(postlist) == 0:
            break
        i += 1


def get_postcontent(url):
    docid = url.split('/')[-1][:9]
    r = requests.get(url)
    time.sleep(random.uniform(0, 1))
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    print(f'doc{docid}.txt')
    with open(f'posts/doc{docid}.txt', 'w') as fp:
        fp.write('<title>\n')
        fp.write(soup.find('li', {'class': 'title'}).get_text())
        fp.write('</title>\n')
        fp.write('<content>\n')
        try:
            fp.write(soup.find('div', {'class': 'article-content'}).get_text())
        except AttributeError:
            pass
        fp.write('</content>\n')
        fp.write('<tag>\n')
        try:
            fp.write(soup.find('div', {'class': 'article-keyword'}).get_text())
        except AttributeError:
            pass
        fp.write('</tag>\n')
        fp.write('<url>\n')
        fp.write(url)
        fp.write('</url>\n')


def html2data(html, url, docid):
    soup = BeautifulSoup(html, 'html.parser').extract()
    data = dict()
    data['id'] = docid
    data['url'] = url
    data['title'] = soup.find('li', {'class': 'title'}).get_text().strip()
    content = soup.find('div', {'class': 'article-content'})
    data['content'] = content.get_text()
    data['img_count'] = len(content.find_all('img'))
    try:
        data['tag'] = soup.find('div', {'class': 'article-keyword'}).get_text().strip()
    except:
        pass
    data['author'] = soup.find('a', {'class': 'author-profile__name'}).get_text().strip()
    data['comment'] = [comm.get_text().strip() for comm in soup.find_all('li', {'class': 'post-text'})]
    return data


def postcontent2pickle(url):
    docid = url.split('/')[-1][:9]
    print(f'doc{docid}.txt')
    r = requests.get(url)
    time.sleep(random.uniform(0, 1))
    r.encoding = 'utf-8'
    open(f'new_htmls/doc{docid}.html', 'w').write(r.text)
    try:
        pickle.dump(html2data(r.text, url, docid), open(f'new_post_pickles/doc{docid}.pickle', 'wb'))
    except:
        pass


def get_top_post(url):
    i = 1
    while True:
        #r = requests.get(f'https://www.pixnet.net/blog/articles/category/26/latest/{i}')
        r = requests.get(f'{url}/{i}')
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        c = 0
        for x in soup.find_all('div', {'class': 'more'}):
            if '繼續閱讀' in x.text:
                #get_postcontent(x.get('href'))
                postcontent2pickle(x.find('a').get('href'))
                c += 1
        if c == 0:
            break
        i += 1
        print(i)
        if i > 2:
            break


def main():
    for w in listdir('htmls'):
        html = open('htmls/'+w).read()
        soup = BeautifulSoup(html, 'html.parser')
        for x in soup.find_all('li'):
            if '個人分類' in x.text:
                #get_postcontent(x.get('href'))
                print(x.find('a').get('href'))
                get_top_post(x.find('a').get('href'))
                #postcontent2pickle(x.get('href'))
        #get_top_post(url)


if __name__ == '__main__':
    main()
