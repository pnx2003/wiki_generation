import requests
import re
import os
from config import parse_args
from bs4 import BeautifulSoup
from tqdm import tqdm
from craw_data import google_spider
def url2doc(url):
    try:
        # if the get takes too long, it will return None
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            text = response.text
        else:
            return None
    except Exception as e:
        print(e)
        return None
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

def is_bad_line(line):
    # remove the line that doesn't end with punctuations
    ending_punctuations = ['.', '?', '!', ':', ',',"\"", "\'"]
    if not any(line.endswith(p) for p in ending_punctuations):
        return True
    
    # remove the line that contains only a few words
    if len(line) < 5:
        return True
    
    # remove the line if it contains ill_word_regrex
    ill_word_regrex = "[-]|□|■|�"
    if re.search(ill_word_regrex, line) != None:
        return True
    
    return False

def is_bad_doc(args, badword_filepath):
    
    # remove the doc that contains bad words more than bad_words_ratio
    def func(doc):
        if len(doc) == 0:
            return True
        bad_word_character_count = 0
        for bad_word in open(badword_filepath, 'r'):
            bad_word = bad_word.strip()
            if bad_word in doc:
                bad_word_character_count += len(bad_word) * doc.count(bad_word)
                
        if bad_word_character_count / len(doc) > args.bad_words_ratio:
            return True
        return False
    return func


def filter_out_bad_lines(args):
    with open(args.raw_data, 'r') as f:
        docs = f.read().split('\n')
    is_bad_docs = map(is_bad_doc(args, args.badword_filepath), docs)
    
    # remove the bad docs
    docs = [doc for doc, is_bad in zip(docs, is_bad_docs) if not is_bad]
    all_lines = map(lambda doc: re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', doc), docs)
    docs_new = []
    for lines in tqdm(all_lines):
        is_bad_lines = map(is_bad_line, lines)
        badlines = [line for line, is_bad in zip(lines, is_bad_lines) if is_bad]
        lines = [line for line in lines if line not in badlines]
        doc = ''.join(lines)
        docs_new.append(doc)
        with open('tmp/bad_line.txt','a') as f:
            f.write('\n'.join(badlines))

    with open(args.clean_data, 'w') as f:
        f.write('\n'.join(docs_new))


# remove the duplicate text
def remove_duplicate_text(args):
    with open(args.clean_data, 'r') as f:
        docs = f.read().split('\n')
    docs = list(set(docs))
    all_lines = list(map(lambda doc: re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', doc), docs))
    
    def remove_duplicate_lines(lines):
        return ''.join(list(set(lines)))
    
    docs = list(map(remove_duplicate_lines, all_lines))
    return docs
       
# get the clean data
def clean_data(args):
    if not os.path.exists(args.raw_urls):
        print(f'raw_urls for {args.keyword} does not exist, start to crawl the urls')
        google_spider(args.keyword,args.page, args.raw_urls)

    with open(args.raw_urls, 'r') as f:
        urls = f.read().split('\n')
    # remove https://en.wikipedia.org/wiki/Albert_Einstein

    # remove the wiki file for keyword.
    search_keyword = args.keyword.replace(' ', '_')
    urls.remove(f'https://en.wikipedia.org/wiki/{search_keyword}')
    docs = []
    if not os.path.exists(args.raw_data):
        for url in tqdm(range(len(urls))):
            doc = url2doc(urls[url])
            # save the doc as one line
            if doc is not None:
                doc = doc.replace('\n', ' ')
                docs.append(doc)
        
        with open(args.raw_data, 'w') as f:
            f.write('\n'.join(docs))
       
    print(f'raw_data for {args.keyword} exists, the path is {args.raw_data}')
    print(f'clean_data for {args.keyword} exists, the path is {args.clean_data}')
    filter_out_bad_lines(args)
    docs = remove_duplicate_text(args) 
    with open(args.clean_data, 'w') as f:
        f.write('\n'.join(docs))   
    return docs


if __name__ == '__main__':
    args = parse_args()
    keyword_key = args.keyword.lower().replace(' ', '_')
    args.data_path = os.path.join(args.data_path, keyword_key)
    args.raw_urls = os.path.join(args.raw_urls, f'{keyword_key}.txt')
    if not args.raw_data:
        args.raw_data = 'tmp/tmp.txt'
        args.clean_data = 'tmp/tmp_clean.txt'
    clean_data(args)

        
        