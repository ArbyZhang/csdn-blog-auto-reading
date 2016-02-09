#!/usr/bin/env python3
# -*-encoding=utf8 -*-

import urllib.request
import bs4
import re

def html_downloader(url):
    try:
        request = urllib.request.Request(url)
        request.add_header('user-agent', 'Mozilla/5.0')
        response = urllib.request.urlopen(request)
    
        return response.read()
    except:
        print('html_downloader failed')
        exit(0)

def max_article(blog_name):

    root = 'http://blog.csdn.net/'+blog_name
    print('总入口地址: %s\n' % root)

    html_cnt = html_downloader(root)

    soup = bs4.BeautifulSoup(html_cnt, 'html.parser', from_encoding='utf-8')

    try:
        max_al = soup.find('a', text='尾页')['href'].split("/")[-1]
    except:
        max_al = 1
    
    return int(max_al)

def html_parser(blog_name, max_al):

    url_set = set()
    article_list_set = set()

    all_count = 0

    for num in range(1, max_al+1):
        article_list_set.add(r'http://blog.csdn.net/%s/article/list/%d' % (blog_name, num))

    for URL in article_list_set:

        print(URL)
        
        count = 0

        html_cnt = html_downloader(URL)

        soup = bs4.BeautifulSoup(html_cnt, 'html.parser', from_encoding='utf-8')

        soup = soup.find('div', class_='list_item_new')

        links = soup.find_all('a', href=re.compile(r'/article/details'))
    
        for link in links:
            if '#comments' in link['href']:
                pass
            else:
                link = 'http://blog.csdn.net' + link['href']
                if link not in url_set:
                    url_set.add(link)
                    print(link)
                    count += 1

        all_count += count
        print('单页数量: %d\n' % count)

    print('总数量: %d\n\n' % all_count)

    return url_set

def main():

    frequency_time = input('frequency: ')
    frequency_time = int(frequency_time)

    blog_name = input('blog\'s name: ')

    max_al = max_article(blog_name)
    url_set = html_parser(blog_name, max_al)

    print('detial:')
    for url in url_set:
        for i in range(0, frequency_time):
            html_downloader(url)
            print('%s, %d' % (url, i+1))
        print()



if __name__ == '__main__':
    main()
