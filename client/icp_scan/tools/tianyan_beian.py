# -*- coding: utf-8 -*-
import requests,sys
from bs4 import BeautifulSoup

def domainget(id, cookie):
    tianyan_icp_url = "https://www.tianyancha.com/pagination/icp.xhtml?TABLE_DIM_NAME=icp&ps=10&pn=1&id={}".format(id)
    header={
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
        "Cookie":cookie,
    }
    icp_result = requests.get(tianyan_icp_url, headers=header)
    soup = BeautifulSoup(icp_result.text, 'html.parser')
    result = ""
    for line in soup.find_all('span'):
        if('ICP' in str(line) and '号' in str(line)):
            if("-" in str(line)):
                result = str(line).split('<span>')[1].split('-')[0]
            else:
                result = str(line).split('<span>')[1].split('</span>')[0]

    icplishi_url = "https://icplishi.com/{}/".format(result)
    header={
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
    }
    icplishi_result = requests.get(icplishi_url, headers=header)
    soup = BeautifulSoup(icplishi_result.text, 'html.parser')
    target = soup.find_all("span")[2:-3]
    urls = soup.find_all("a")[1:]
    for i in urls:
        if (result in str(i)):
            urls.remove(i)

    l = len(target)
    lastresult = []
    for i in range(0,l):
        #print(str(target[i]).split('<span>')[1].split('</span>')[0] + "\t" + str(urls[i]).split('_blank">')[1].split('</a>')[0])
        lastresult.append((str(target[i]).split('<span>')[1].split('</span>')[0],str(urls[i]).split('_blank">')[1].split('</a>')[0]))

    # print("=================================================")
    # for i in lastresult:
    #     print(i[1])
    
    return lastresult



if __name__ == '__main__':
    id = sys.argv[1]
    cookie = sys.argv[2]
    print(domainget(id, cookie))

