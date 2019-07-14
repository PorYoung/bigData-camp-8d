import requests
from bs4 import BeautifulSoup
import random
import hashlib
import time
import json
from string import Template

runTimes = 10
waitTime = 5
jobDict = {}
dataTemplate = '> 工作名称<span id="${jobNumber}"></span>\n\n`${jobName}`\n\n> 公司\n\n[${companyName}](${companyUrl})\n\n![Logo](${companyLogo}#logoImg)\n\n`${companyType}`\n\n> 城市\n\n`${city}`\n\n> 学历要求\n\n`${eduLevel}`\n\n> 薪资\n\n`${salary}`\n\n> 福利\n\n${welfare}\n\n---\n\n'


def spider_zhilian_content(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    print(response.status_code)

    if response.status_code == 200:
        response.encoding = 'utf-8'
        respJson = response.json()
        # data = json.loads(respJson['data'])
        data = respJson['data']['results']

        content = ''

        for item in data:
            jobDict[item['jobName']] = item['number']
            welfare = ''
            for w in item['welfare']:
                welfare += '`'+w+'` '
            new_data = Template(dataTemplate).substitute(jobName=item['jobName'], jobNumber=item['number'], companyName=item['company']['name'], companyUrl=item['company']['url'], companyLogo=item[
                'companyLogo'], companyType=item['company']['type']['name'], city=item['city']['display'], eduLevel=item['eduLevel']['name'], salary=item['salary'], welfare=welfare)
            content += new_data
        return content

# 随机生产请求参数
def params_generator(times):
    _v = str(random.random())[0:10]
    hl = hashlib.md5()
    hl.update(_v.encode(encoding='utf-8'))
    cid = str(hl.hexdigest())
    cid = cid[0:8]+'-'+cid[8:12]+'-'+cid[12:16]+'-'+cid[16:20]+'-'+cid[20:32]
    hl.update(cid.encode(encoding='utf-8'))
    prid = str(hl.hexdigest())+_v[2:7]

    start = times*90

    return {
        "start": start,
        "pageSize": 90,
        "cityId": 489,
        "salary": "0,0",
        "workExperience": -1,
        "education": -1,
        "companyType": -1,
        "employmentType": -1,
        "jobWelfareTag": -1,
        "kw": "大数据",
        "kt": 3,
        "_v": _v,
        "x-zp-page-request-id": prid,
        "x-zp-client-id": cid
    }


headers = {
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://sou.zhaopin.com/?jl=489&sf=0&st=0&kw=%E5%A4%A7%E6%95%B0%E6%8D%AE&kt=3",
    "Origin": "https://sou.zhaopin.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}
url = 'https://fe-api.zhaopin.com/c/i/sou'

times = 0
spider_time_start = time.time()

# if __name__ == 'main':
f = open('zhilian.md', 'a+', encoding='utf-8')

totalContent = '## 数据列表\n\n'
while(times < runTimes):
    params = params_generator(times)
    content = spider_zhilian_content(url, headers, params)
    totalContent += content
    time.sleep(waitTime)
    times += 1
spider_time_end = time.time()
spider_count_time = spider_time_end-spider_time_start-runTimes*waitTime

imgStyle = '<style>img[src*="logoImg"]{width:100px;height:100px}</style>\n\n'
jobIndex = '> 爬取关键字：`大数据`\n> 爬取数据量：`' + \
    str(len(jobDict))+'`\n去除等待时间('+str(runTimes*waitTime) + \
    's)爬取时间：`'+str(spider_count_time)+'`\n\n## 目录\n\n'

for k, v in jobDict.items():
    jobIndex += '- ['+k+'](#'+v+')\n'
jobIndex += '\n---\n\n'

f.write(imgStyle+jobIndex+totalContent)
f.close()
