import re
import urllib3
import time
import requests
import socket
import csv
from bs4 import BeautifulSoup
from tqdm import tqdm

# ignore https certificate warning
urllib3.disable_warnings() 



# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

def google_spider(query, page, file_name):
    num = 1
    query = query.replace(' ', '+')
    for num in tqdm(range(page)):
        URL = f"https://www.google.com.hk/search?q={query}&newwindow=1&hl=zh-CN&ei=MSEaYcmdH9TW-QaTr7aIBg&start={num}&sa=N&ved=2ahUKEwiJ-vanj7XyAhVUa94KHZOXDWE4FBDw0wN6BAgBEEU&biw=1366&bih=773"

        # try:
        headers = {"user-agent": USER_AGENT}
        proxies = {'http':'http://127.0.0.1:7890'}
        resp = requests.get(URL, headers=headers, verify=False,proxies=proxies)
        time.sleep(0.1)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")

            results = []
            
            # url is in the href value of <a> tag under <div> tag
            for g in soup.find_all('div'):  # <div>
                anchors = g.find_all('a')  # <a href="">
                if anchors:
                    for i in range(len(anchors)):
                        try:
                            link = anchors[i].attrs['href']  # extract the content of the dictionary

                            # regular expression to filter URL, delete some garbled code
                            if re.match('/', link) is None and re.match('(.*)google.com',
                                                                        link) is None and link != '#' and link.find(
                                'search?q') == -1:

                                # filter out duplicate URLs
                                for i in results:
                                    if i.split(".site")[0] == link.split(".site")[0]:
                                        link = ""
                                results.append(link)
                        except:
                            pass
                        
        # save the result to the result folder
        with open(f"{file_name}",mode="a+") as f:
            for i in results:
                if i != '':
                    f.write(i + "\n")
                    
        print(f'finish {num} page')

