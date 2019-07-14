import _csv
import requests
import random
import hashlib
import re

from zhilian_ms import ZhilianMS

from pyquery import PyQuery as pq
# from pyquery import PyQuery


class ZhiLian:
    def __init__(self, *args, **kwargs):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://sou.zhaopin.com/?jl=489&sf=0&st=0&kw=%E5%A4%A7%E6%95%B0%E6%8D%AE&kt=3",
            "Origin": "https://sou.zhaopin.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
        self.url = 'https://fe-api.zhaopin.com/c/i/sou'
        self.f = open('spider-zhilian.csv', 'w', encoding='utf-8')
        self.out = _csv.writer(self.f)
        self.out.writerow(['工作ID', '工作名', '公司名', '公司Url', '公司Logo', '公司类型',
                           '城市', '学历要求', '薪资', '福利', '招聘人数', '工作亮点', '职位描述', '技能要求'])
        _v = str(random.random())[0:10]
        hl = hashlib.md5()
        hl.update(_v.encode(encoding='utf-8'))
        cid = str(hl.hexdigest())
        cid = cid[0:8]+'-'+cid[8:12]+'-' + \
            cid[12:16]+'-'+cid[16:20]+'-'+cid[20:32]
        hl.update(cid.encode(encoding='utf-8'))
        prid = str(hl.hexdigest())+_v[2:7]
        self._v = _v
        self.cid = cid
        self.prid = prid

    # 产生请求参数
    def params_generator(self, times, keyword):
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
            "kw": keyword,
            "kt": 3,
            "_v": self._v,
            "x-zp-page-request-id": self.prid,
            "x-zp-client-id": self.cid
        }

    def getJsonData(self, params):
        response = requests.get(self.url, headers=self.headers, params=params)
        if response.status_code == 200:
            response = response.json()
            return response['data']['results']
        return False

    def getDetailData(self, url):
        response = requests.get(url)

        if response.status_code == 200:
            response.encoding = 'utf-8'
            d = pq(response.text)
            """ print(len(d('#nocaptcha .nc_iconfont.btn_slide')))
            # 需要验证
            if len(d('#nocaptcha .nc_iconfont.btn_slide')) > 0:
                zlms = ZhilianMS(url)
                flag, html = zlms.start_simulate()
                zlms.close()
                print('?')
                if flag == True:
                    d = pq(html)
                else:
                    # 验证失败
                    return '', '', '', '' """
            # 招收人数
            recruit = d(
                '.summary-plane .summary-plane__info li:last').text()[1:-1]
            """ if len(recruit) == 0:
                # ff = open('imgCaptcha.htm', 'r+', encoding='utf-8')
                # if len(ff.read()) == 0:
                #     ff.write(response.text)
                # ff.close()

                zlms = ZhilianMS(url)
                flag, html = zlms.start_simulate(time=0.1)
                zlms.close()
                if flag == True:
                    d = pq(html)
                else:
                    # 验证失败
                    return '', '', '', '' """
            # 职位亮点
            # highlight = d('.a-center-layout__content .highlights__content').text().split(' ')
            highlightList = d(
                '.a-center-layout__content .highlights__content span')
            highlight = []
            for i in highlightList.items():
                highlight.append(i.text())
            # 职位描述
            describe = d(
                '.describtion .describtion__detail-content').text().strip('\n')
            # 技能要求
            skill = d(
                '.description .describtion__skills-content').text().split(' ')
            return recruit, highlight, describe, skill

    def parseData(self, jsonData):
        for item in jsonData:
            # try:
            list = []
            jobNumber = item['number']
            jobName = item['jobName']
            companyName = item['company']['name']
            companyUrl = item['company']['url']
            companyLogo = item['companyLogo']
            companyType = item['company']['type']['name']
            city = item['city']['display']
            eduLevel = item['eduLevel']['name']
            salary = item['salary']
            welfare = item['welfare']

            (recruit, highlight, describe, skill) = self.getDetailData(
                item['positionURL'])

            list.extend([jobNumber, jobName, companyName, companyUrl, companyLogo, companyType,
                         city, eduLevel, salary, welfare, recruit, highlight, describe, skill])

            self.out.writerow(list)

            # except:
            #     print('function:parseData Error!')
        # self.f.close()
    def fclose(self):
        self.f.close()


zl = ZhiLian()
for times in range(0, 10):
    data = zl.getJsonData(zl.params_generator(times, '大数据'))
    if(data == False):
        pass
    else:
        zl.parseData(data)
for times in range(0, 10):
    data = zl.getJsonData(zl.params_generator(times, 'Python'))
    if(data == False):
        pass
    else:
        zl.parseData(data)
for times in range(0, 10):
    data = zl.getJsonData(zl.params_generator(times, 'Java'))
    if(data == False):
        pass
    else:
        zl.parseData(data)
zl.fclose()
