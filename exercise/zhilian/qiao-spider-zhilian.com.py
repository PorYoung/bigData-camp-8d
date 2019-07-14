import requests
import time
# import json
import random
import hashlib
import urllib.parse
from string import Template

category = 'Java'
keyword = urllib.parse.quote(category)
timestamp = int(round(time.time() * 1000))
md5 = hashlib.md5(str(timestamp).encode('utf-8')).hexdigest()

url = Template('https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=551&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=${kw}&kt=1000000&_v=${_v}&x-zp-page-request-id=${md5}-${ts}-${random}&x-zp-client-id=9d6a8864-b52a-4914-ba69-d0aedab8089b').substitute(kw=keyword, _v=str(random.random())[0:10], md5=md5, ts=timestamp, random=random.uniform(100000, 999999))
print(url)
r = requests.get(url)
r.encoding = 'utf-8'
data = r.json()
# with open('mock_data.txt', 'r', encoding='utf-8') as file:
# data = json.loads(file.read())
if data['code'] == 200:
    opu = data['data']['results']
    txtName = category + '.txt'
    f = open(txtName, 'a+', encoding='utf-8')
    for i in range(0, len(opu)):
        item = opu[i]
        new_item_data = Template('${number}\r\n岗位名称 ${jobName}\r\n公司名称 ${comName}\r\n薪资 ${salary}\r\n办公地址 ${businessArea}\r\n学历要求 ${eduLevel}\r\n-----------\r\n').substitute(number=item['number'], jobName=item['jobName'], comName=item['company']['name'], salary=item['salary'], businessArea=item['businessArea'], eduLevel=item['eduLevel']['name'])
        f.write(new_item_data)
    f.close()