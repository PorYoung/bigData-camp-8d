import requests
from bs4 import BeautifulSoup

def spider_xiaohuar_content(url, headers):
    response = requests.get(url=url, headers=headers)

    print(response.status_code)

    if response.status_code == 200:
        response.encoding = 'utf-8'
        html = response.content
        # 参数：网页内容，解析器
        soup = BeautifulSoup(html, 'html5lib')
        div_list = soup.find_all('div', attrs={'class': 'all_lanmu'})

        text = ''
        file = open('爬虫校花.md', 'w', encoding='utf-8')
        for div in div_list:
            title_div = div.find('div', attrs={'class': 'title1000'})
            title = title_div.find('a').string
            text += '<style>img[src*="headimg-style"]{width:100px;height:100px}</style>\n\n## 标题：'+title+'\n\n'

            ul = div.find('ul')
            li_list = ul.find_all('li')
            for li in li_list:
                img_src = li.find('img').attrs['lazysrc']
                a_href = li.find('a').attrs['href']
                img_title = li.find('span').string
                school = li.find('b', attrs={'class': 'b1'}).string
                fav = li.find('b', attrs={'class': 'b2'}).string

                if url not in img_src:
                    img_src = url+img_src
                text += '> ' + img_title+'\n\n'
                text += '!['+img_title+']('+img_src+'#headimg-style)'+'\n\n'
                text += '- 学校：'+school+'\n\n'
                text += '- 点赞人数:'+fav+'\n\n'
        file.write(text)
        file.close

url = 'http://xiaohuar.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
spider_xiaohuar_content(url, headers)