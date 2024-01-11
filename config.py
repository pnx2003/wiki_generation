import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    #parser.add_argument('--data_path', type=str, default='./data')
    parser.add_argument('--data_path', type=str, default='./data_new',help='the path of the data processed')
    parser.add_argument('--key_words_path', type=str, default='./keywords',help='the path of the keywords')
    parser.add_argument('--temp_path', type=str, default='./templates',help='the path of the templates')
    #parser.add_argument('--raw_data', type=str, default='enwiki.utf8.txt')
    parser.add_argument('--raw_data', type=str, default=None,help='the path of the raw data')
    parser.add_argument('--retrieve_model', type=str, default='BM25',help='The type of the retrieve model')
    parser.add_argument('--rerank_model', type=str, default='CoROM',help='The type of the rerank model')
    parser.add_argument('--LLM', type=str, default='GPT4-Turbo-128',help='the type of the LLM')
    parser.add_argument('--type', type=str, default='university',help='the type of the keyword')
    parser.add_argument('--keyword', type=str, default='Carnegie Mellon University', help='the keyword')
    parser.add_argument('--topn1', type=int, default=600, help='the number of the retrieve results')
    parser.add_argument('--topn2', type=int, default=500, help='the number of the rerank results')
    parser.add_argument('--raw_urls', type=str, default='./result', help='the path of the raw urls')
    parser.add_argument('--badword_filepath', type=str, default='./data_new/badwords.txt', help='the path of the bad words')
    parser.add_argument('--bad_words_ratio', type=float, default=0.05, help='the ratio of the bad words')
    parser.add_argument('--clean_data', type=str, default='./data_new.txt', help='the path of the clean data')
    parser.add_argument('--output_path', type=str, default='./output', help='the path of the output')
    parser.add_argument('--page',type=int,default=100,help='the page of the search engine')
    args = parser.parse_args()
    return args



