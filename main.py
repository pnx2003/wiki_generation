from config import parse_args
from generate_structure import generate_structure_template
import os
from dataHelper import get_data
from generate_wiki import generate_wiki
 

def main():
    args = parse_args()
    keyword_key = args.keyword.lower().replace(' ', '_')
    args.data_path = os.path.join(args.data_path, keyword_key)
    args.raw_urls = os.path.join(args.raw_urls, f'{keyword_key}.txt')
    args.output_path  = os.path.join(args.output_path, keyword_key)
    if not os.path.exists(args.data_path):
        os.makedirs(args.data_path)
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    if not os.path.exists(os.path.join(args.data_path,'rerank')):
        os.makedirs(os.path.join(args.data_path,'rerank'))
    if not os.path.exists(os.path.join(args.data_path,'retrieve')):
        os.makedirs(os.path.join(args.data_path,'retrieve'))
        
    
    if not args.raw_data:
        args.raw_data = os.path.join(args.data_path, f'{keyword_key}_raw.txt')
        args.clean_data = os.path.join(args.data_path, f'{keyword_key}_clean.txt')
    
    # reranked data for keyword    
    data = get_data(args)
    
    # get the template for keyword
    with open(f'{args.temp_path}/{args.type}_template.out', 'r') as f:
        template = f.read().split('\n')
    prompts = {}
    
    for t in template:
        key, value = t.split(':')[0], t.split(':')[1].lower()
        prompts[key] = value
    
    # generate the structure for keyword
    result = generate_wiki(data, args.LLM, prompts, args.keyword, args.output_path)
    return 

    
    
    
    
    
    
if __name__ == '__main__':
    main()