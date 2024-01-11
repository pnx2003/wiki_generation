"""
generate structure template from wikipedia according to keywords we defined
"""
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def crawl_baike(url):

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(e)
    

def parse_document(document):
    soup = BeautifulSoup(document, 'html.parser')
    # 在这里添加解析HTML的代码，提取出章节结构，可以使用soup.select等方法
    # 返回章节标题的列表
    titles = []
    for tag in soup.find_all(re.compile(r'h\d')):
        titles.append(tag.text)
    return titles

def generate_structure_template(keywords):
    templates = {}
    titless = []
    for keyword in keywords:
        doc = crawl_baike(keywords[keyword])
        titles = parse_document(doc)
        # delete the keyword if it is include in title, title is a string
        for i, title in enumerate(titles):
            if keyword in title:
                # remove the substr keyword in title
                titles[i] = title.replace(keyword, '')
                # if title[i]=='', remove it
                if titles[i] == '':
                    titles.remove('')
            
        titless += titles
        
    title_counts = Counter(titless)
    print(title_counts)
    #print(title_counts)
    most_common_titles = title_counts.most_common(15)  # choose 15 most common tytles
    templates = [title for title, _ in most_common_titles]
    print(templates)
    return templates

if __name__ == "__main__":
    import argparse
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, default='scientists')
    parser.add_argument('--temp_path', type=str, default='./templates')
    parser.add_argument('--keywords_path', type=str, default='./keywords')

    args = parser.parse_args()
    with open(f'{args.keywords_path}/{args.type}.txt', 'r') as f:
        keywords = f.read().split('\n')
    
    
    key_url_dict = {key:url for key, url in [keyword.split('#') for keyword in keywords if keyword != '']}
    template = generate_structure_template(key_url_dict)
    # dump structure_templates to file "structure_templates.out"
    with open(f'{args.temp_path}/{args.type}_template.out', 'w') as f:
        # save the list, each element in one line
        f.write('\n'.join(template))
    
        

    # 打印生成的结构模板
