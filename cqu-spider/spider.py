import requests
from pyquery import PyQuery as pq
import csv
from time import sleep
# import re


class CquSpider:
    def __init__(self, config):
        self.url = config['url']
        self.headers = config['headers']

    def getList(self, page):
        res = requests.get(self.url + 'list-24-' + str(page) +
                           '.html', headers=self.headers)
        res.encoding = 'utf-8'
        return res.text

    def parseList(self, text):
        d = pq(text)
        lists = d('.container.newslist .lists .item')
        content = ''
        for item in lists.items():
            # title <a/>
            atag = item('.title a')
            category = ''
            title = ''
            url = ''
            for a in atag.items():
                if(a.attr['style'] == None):
                    title = a.text().strip('\t')
                    url = a.attr['href']
                    if(url == None):
                        url = ''
                else:
                    category = a.text().strip('\t')
            # speaker
            speaker = item('.minfo p').eq(0)
            speaker.remove('strong')
            speaker = speaker.text().strip('\t')

            # date
            date = item('.minfo p').eq(1)
            date.remove('strong')
            date = date.text()
            date = date[0:4] + '-' + date[5:7] + '-' + date[8:10]
            content += '\t'.join([title, category, speaker, date, url]) + '\n'
        return content

    def listSpider(self, path, page=1, mode='w'):
        with open(path, mode, encoding='utf-8') as f:
            # f = open(path, mode, encoding='utf-8')
            f.write('title\tcategory\tspeaker\tdate\turl\n')
            for p in range(1, page+1):
                text = self.getList(p)
                content = self.parseList(text)
                f.write(content)
            # f.close()

    def getDetail(self, url):
        res = requests.get(url, headers=self.headers)
        res.encoding = 'utf-8'
        return res.text

    def urlReader(slef, path):
        urls = []
        dates = []
        with open(path, encoding='utf-8') as cf:
            c_r = csv.reader(cf, delimiter='\t')
            line = 0
            for row in c_r:
                if(line == 0):
                    line += 1
                    continue
                if(row[4] != ''):
                    urls.append(row[4])
                    dates.append(row[3][0:7])
        return urls, dates

    def detailSpider(self, infoPath):
        urls, dates = self.urlReader(infoPath)
        for i in range(0, len(urls)):
            text = self.getDetail(urls[i])
            if text == '':
                continue
            d = pq(text)
            content = d('.content .acontent')
            content.remove('img')
            content = content.text()
            # 阅读量
            tid = urls[i].split('-')
            if(len(tid) >= 2):
                tid = tid[-2]
                hitsUrl = 'http://news.cqu.edu.cn/newsv2/api.php?op=count&id=' + tid + '&modelid=29'
                res = requests.get(hitsUrl, headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Host': 'news.cqu.edu.cn',
                    'Referer': urls[i],
                    'Proxy-Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'max-age=0',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
                })
                res.encoding = 'utf-8'
                hits = res.text[res.text.rfind('(')+2:res.text.rfind(')')-1]
                if(int(hits) > 100000):
                    hits = '-1'
                with open('out/hits.csv', 'a+', encoding='utf-8') as f:
                    f.write(hits+'\n')
                sleep(0.1)
            # with open('out/'+dates[i]+'.txt', 'a+', encoding='utf-8') as f:
            #     f.write(content + '\n======\n')


if __name__ == '__main__':
    config = {
        'url': 'http://news.cqu.edu.cn/newsv2/',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
    }
    cqu = CquSpider(config)

    # cqu.listSpider('out/cqu_info_list.csv', 29, 'w')
    cqu.detailSpider('out/cqu_info_list.csv')
