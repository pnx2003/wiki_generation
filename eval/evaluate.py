import requests
from bs4 import BeautifulSoup

# def crawl_baidu_baike(url):
#     # 发送HTTP请求
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # 假设每个章节的标题是h2标签，内容在紧随其后的div标签中
#     for title in soup.find_all('h2'):
#         print(title.get_text().strip())  # 打印章节标题
#         content = title.find_next_sibling('div')
#         if content:
#             print(content.get_text().strip())  # 打印章节内容

# # 使用示例
# url = 'https://baike.baidu.com/link?url=es55ahCH3viYhHK0VlLXjFql6jSFWW0VnPCTeh3TAKKFdgYFBPsGH_VvbpJkZkBDRlYynVvllDngLpM1Ki_OCFnI_iYsVvwSlFtMQiFG2MrVpi5mJAbhXB09jwrbrDegXx__Qf-CGseGC4UskzGYbG2YDeN-Cyo0a4AAzF7_5ZtpNRJawA646eVhfer_fHbK'
# crawl_baidu_baike(url)

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from collections import Counter
import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel

def calculate_ttr(tokens):
    """ 计算类型-标记比（TTR） """
    types = set(tokens)
    return len(types) / len(tokens)

def topic_coverage(tokens, num_topics=5):
    """ 分析文档的话题覆盖 """

    tokens = [tokens]
    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(token) for token in tokens]
    lda = LdaModel(corpus, num_topics=num_topics, id2word=dictionary)
    return lda.show_topics()

def evaluate_informativeness(document):
    """ 评估文档的信息性 """
    ttr = calculate_ttr(document)
    topics = topic_coverage(document)
    return {
        "TTR": ttr,
        "topics_coverage": topics
    }

# 使用示例
# document_text = "这里是文档的文本内容..."
# informativeness_report = evaluate_informativeness(document_text)
# print("词汇多样性（TTR）:", informativeness_report["词汇多样性（TTR）"])
# print("话题覆盖:")
# for topic in informativeness_report["话题覆盖"]:
#     print(topic)

if __name__ == '__main__':
    keyword = 'albert_einstein'
    with open('./templates/scientists_template.out', 'r') as f:
        templates = f.read().split('\n')
        
    
    for i,template in enumerate(templates):
        key, value = template.split(':')
        templates[i] = key.lower().replace(' ', '_')
        
    for template in templates:
        with open(f'./output/{keyword}/{template}.txt', 'r') as f:
            text = f.read()
            tokens = word_tokenize(text.lower())
            #去掉标点
            tokens = [token for token in tokens if token.isalpha()]
            #去掉停用词
            stopwords = nltk.corpus.stopwords.words('english')
            stopwords.extend(['\'s','*','albert','einstein'])
            tokens = [token for token in tokens if token not in stopwords]
            informativeness_report = evaluate_informativeness(tokens)
            print('------------------')
            print(template)
            print("TTR:", informativeness_report["TTR"])
            print("topics coverage:")
            for topic in informativeness_report["topics_coverage"]:
                print(topic)