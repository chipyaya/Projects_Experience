# coding: utf-8
from bs4 import BeautifulSoup
import pickle
import requests
import re
import os
import os.path
import urllib.request
import sys

ptt_url = 'https://www.ptt.cc'
def get_webpage(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def parse_post(webpage):
    soup = BeautifulSoup(webpage, 'html.parser')
    links = soup.find(id='main-content').find_all('a')
    img_urls = []
    blog_url = ''
    for link in links:
        if re.match(r'^.*jpg', link['href']):
            img_urls.append(link['href'])
        elif re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):
            img_urls.append(link['href'])
        elif 'pixnet.net' in link['href']:
            blog_url = link['href']
    return img_urls, blog_url

def save(img_urls, dir_name):
    try:
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        index = 0
        for img_url in img_urls:
            if index >= 5:
                break
            if re.match(r'^https?://(i.)?(m.)?imgur.com', img_url):
                if img_url.split('//')[1].startswith('m.'):
                    img_url = img_url.replace('//m.', '//i.')
                if not img_url.split('//')[1].startswith('i.'):
                    img_url = img_url.split('//')[0] + '//i.' + img_url.split('//')[1]
                if not img_url.endswith('.jpg'):
                    img_url += '.jpg'
            fname = f'{index}.jpg'
            index += 1
            urllib.request.urlretrieve(img_url, os.path.join(dir_name, fname))
    except Exception as e:
        print(e)
        pass

def get_imgs_blog(webpage):
    soup = BeautifulSoup(webpage, 'html.parser')
    content = soup.find('div', {'class': 'article-content'})

    imgs = content.find_all('img')
    img_urls = []
    for img in imgs:
        img_url = img['src']
        if img_url.endswith('.jpg'):
            img_urls.append(img_url)
    return img_urls

def main():
    ptt_dir = '/tmp2/GorsachiusMelanolophus/ptt_posts_new/no_sponsored/'
    imgs_dir = '/tmp2/GorsachiusMelanolophus/ptt_imgs/no_sponsored/'
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    fp = open('../img_num/' + str(start)+ '.txt', 'a')
    for i in range(start, end):
        try:
            post_path = ptt_dir + str(i) + '.p'
            post = pickle.load(open(post_path, 'rb'))
            url = ptt_url + post['href']
            webpage = get_webpage(url)
            imgs, blog_url = parse_post(webpage)
            if imgs:
                print(f'{i}:{len(imgs)}', file=fp)
                save(imgs, imgs_dir + str(i))
            elif blog_url:
                webpage = get_webpage(blog_url)
                imgs = get_imgs_blog(webpage)
                if imgs:
                    print(f'{i}:{len(imgs)}', file=fp)
                    save(imgs, imgs_dir + str(i))
        except KeyboardInterrupt:
            return 0
        except Exception as e:
            print(e)
            pass
if __name__ == '__main__':
    main()
