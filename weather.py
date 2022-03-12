import requests 
from bs4 import BeautifulSoup
from redis import Redis
import json
redis_config = {
    'host': '1.117.214.111',
    'port': 6379,
    'password': 'ty254731',
    'db': '1'
}
redis = Redis(decode_responses=True, **redis_config)

url = 'http://www.weather.com.cn/weather/101210101.shtml'

rsp = requests.get(url)
html = rsp.content.decode('utf-8')
soup = BeautifulSoup(html, 'lxml')
rst = soup.select('li.sky')

tmp = []
for index, item in enumerate(rst):
	date = item.find('h1').text
	tem_min = item.find('p', class_='tem').find('i').text
	tem_max_ele = item.find('p', class_='tem').find('span')
	tem_max = tem_max_ele.text if tem_max_ele else ''
	if tem_max and (not '℃' in tem_max):
		tem_max = f'{tem_max}℃'
	wea = item.find('p', class_='wea').text
	data = {
		'date':date,
		'wea': wea,
		'tem': f'{tem_min}~{tem_max}' if tem_max else str(tem_min),
	}
	tmp.append(data)

redis.set('hangzhou', json.dumps(tmp, ensure_ascii=False))