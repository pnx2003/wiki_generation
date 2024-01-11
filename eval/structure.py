from nltk.tokenize import sent_tokenize, word_tokenize
import re

def analyze_paragraphs(text):
    """ 段落分析 """
    paragraphs = text.split("\n\n")  # 假设段落由两个换行符分隔
    para_lengths = [len(word_tokenize(p)) for p in paragraphs]
    return para_lengths

def analyze_headings(text):
    """ 标题和小标题分析 """
    headings = re.findall(r'(?<=\*\*).+(?=\*\*)', text) 
    return headings

def evaluate_structure(document):
    """ 评估文档的篇章结构 """
    para_lengths = analyze_paragraphs(document)
    headings = analyze_headings(document)
    #print the result
    print('------------------')
    print("段落长度:", para_lengths)
    print("标题数量:", len(headings))
    return {
        "段落长度": para_lengths,
        "标题数量": len(headings)
    }
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
        evaluate_structure(text)