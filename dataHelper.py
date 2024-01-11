import jieba
import jieba.analyse
import os
from rerank import rerank
from generate_structure import generate_structure_template
from retrieve import retrieve
from clean_data import clean_data
from tqdm import tqdm 

def prepare_data_for_keyword(args):
    if args.clean_data is not None:
        keyword_data_path = args.clean_data
        if os.path.exists(keyword_data_path):
            print(f"clean data for {args.keyword} exists, the path is {keyword_data_path}")
            with open(keyword_data_path, "r", encoding="utf-8") as f:
                paragraphs = f.read().split('\n')
            return paragraphs
        
        return clean_data(args)
    
    else:
        keyword_key = args.keyword.lower().replace(' ', '_')
        keyword_data_path = os.path.join(args.data_path, f"{keyword_key}.txt")
        
        if os.path.exists(keyword_data_path):
            with open(keyword_data_path, "r", encoding="utf-8") as f:
                paragraphs = f.read().split('\n')
            return paragraphs
        
    
        with open(args.raw_data, "r", encoding="utf-8") as f:
            paragraphs = f.read().split('\n')
        #paragraphs = seg_raw_data(args.raw_data, args.seg_data)
        meaningful_paragraphs = [paragraph for paragraph in paragraphs if args.keyword in paragraph]
        
        
        #将段落列表写入到北京大学.txt中
        with open(keyword_data_path, "w", encoding="utf-8") as f:
            f.writelines(meaningful_paragraphs)
            
        return meaningful_paragraphs
        

def retrieve_data_func(args, query, retrieve_data_path):
    
    if os.path.exists(retrieve_data_path):
        print(f"retrieve data for {query} exists, the path is {retrieve_data_path}")
        with open(retrieve_data_path, "r", encoding="utf-8") as f:
            retrieve_data = f.read().split('\n')
        return retrieve_data
    
    query = query[0].replace('and','').split(' ') + query[1].split(',')
    data_for_keyword = prepare_data_for_keyword(args)
    retrieve_data = retrieve(args, data_for_keyword, [query],\
        args.retrieve_model, args.topn1)
    with open(retrieve_data_path, "w", encoding="utf-8") as f:  
        f.write("\n".join(retrieve_data))
    print(f"retrieve data for {query} is saved in {retrieve_data_path}")
    return retrieve_data
    

def rerank_data_func(args, query):
    query = query.lower().split(':')
    query_key = query[0].replace(' ', '_')
    keyword_key = args.keyword.lower().replace(' ', '_')
    rerank_data_path = os.path.join(args.data_path, f"rerank/{query_key}_rerank.txt")
    if os.path.exists(rerank_data_path):
        print(f"rerank data for {query_key} exists, the path is {rerank_data_path}")
        with open(rerank_data_path, "r", encoding="utf-8") as f:
            rerank_data = f.read().split('\n')
        return rerank_data
    
    
    retrieve_data = retrieve_data_func(args, query, rerank_data_path.replace('rerank', 'retrieve'))
    with open(f'queries/queries_{args.type}.txt', 'r') as f:
        prompts = f.read().split('\n')
    for prompt in prompts:
        if query[0] in prompt.lower():
            prompt = prompt.split(': ')[1].replace('NAME', args.keyword)
            break
    return rerank(args, retrieve_data, prompt, keyword_key, query[0].replace(' ','_'), args.rerank_model, args.topn2)

        

def get_data(args):
    # generate the template of this type
    template_path = os.path.join(args.temp_path, f"{args.type}_template.out")
    if not os.path.exists(template_path):
        keywords = []
        with open(os.path.join(args.key_words_path, f"{args.type}.txt"), "r", encoding="utf-8") as f:
            keywords = f.read().split('\n')
        
        #automatically generate the template, another way is to manually write the template
        template = generate_structure_template(keywords)
        with open(template_path, "w", encoding="utf-8") as f:
            f.write("\n".join(template))
    else:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read().split('\n')
    
    
    rerank_datas = {}
    for query in template:
        rerank_data = rerank_data_func(args, query)
        rerank_datas[query.split(':')[0]] = rerank_data
    return rerank_datas

