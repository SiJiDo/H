import csv
import json
import re
import warnings
import argparse
from time import sleep
import sys
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
import os

import requests
from bs4 import BeautifulSoup
import time

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

# 定义查询关键字
q = sys.argv[1]
print(q)

# 定义请求数据部分

def req(qurl):
    # print(qurl)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://grep.app/'

    }

    # 代理
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    # s = requests.Session()
    # # 重试
    # s.mount('http://', HTTPAdapter(max_retries=3))
    # s.mount('https://', HTTPAdapter(max_retries=3))
    try:
        response = requests.get(qurl, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        raise SystemExit(e)
    contents = response.content.decode(response.apparent_encoding, 'ignore')
    json_data = json.loads(contents)
    return json_data


# 解析数据
def parse_datas(json_data):
    urls = []
    hits = json_data['hits']['hits']

    # 正则提取url部分
    # regex = r"(?:&#39;|&quot;)(https?:[/.\w\d]+?\.<mark>" + q + "</mark>.*?)(?:&#39;|&quot;)"
    regex = r"(?:&#39;|&quot;)(https?://[\w]+[.\w\d]+?\.<mark>" + q + "</mark>.*?)(?:&#39;|&quot;)"

    for hit in hits:
        data_content = hit['content']['snippet']
        # git 链接  https://github.com/LubyRuffy/fofa/blob/master/test/workers/workers_test.rb
        repo = hit['repo']['raw']
        gpath = hit['path']['raw']
        rpath = '/blob/master/'
        glink = 'https://github.com/' + repo + rpath + gpath
        # glink= 'http://github.com/'+ gitlink
        # new_glink = glink.replace('/g/', '/')

        matches = re.finditer(regex, data_content)
        for matchNum, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):

                groupNum = groupNum + 1
                group = BeautifulSoup(match.group(groupNum), 'html.parser').get_text()
                if group:
                    urls.append({"url": group, "domain": urlparse(group).netloc, "gitlink": glink})
    return urls

# 存储数据
results = []

# 获取总页数

base_url = 'https://grep.app/api/search?q={}'.format(q)
json_data = req(base_url)
page_count = json_data['facets']['count']  # 所有捕获页数数量

# 第一种情况  只有一页
if page_count <= 10:
    query_url = 'https://grep.app/api/search?q={}'.format(q)
    json_data = req(query_url)
    results = parse_datas(json_data)
    print(results)

# 第二种情况 大于1页
else:
    pages = int(page_count / 10)  # 页数
    for page in range(1, pages, 1):
        query_url = 'https://grep.app/api/search?q={}&page={}'.format(q, page)
        json_data = req(query_url)
        if json_data:
            results = parse_datas(json_data)
            print(results)
        else:
            continue
        if page > 100:  #  最多只能获取100 页
            break
