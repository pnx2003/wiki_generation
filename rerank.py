# from transformers import AutoModelForSequenceClassification
# from transformers import  AutoTokenizer
from transformers import BertTokenizer, BertForQuestionAnswering
import torch
import os
from tqdm import tqdm
from modelscope.models import Model
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import numpy as np
# Version less than 1.1 please use TextRankingPreprocessor
from modelscope.preprocessors import TextRankingTransformersPreprocessor

def CoROM(args, paragraphs, query, keyword, outline, topn2=300):
    print(f"rerank according to {query}")
    if os.path.exists(path=f'{args.data_path}/rerank/{outline}_rerank.txt'):
        with open(f'data/{keyword}/{outline}_rerank.txt', 'r') as f:
            return f.read().split('\n')
    
    model_id = "damo/nlp_corom_sentence-embedding_english-base"
    pipeline_se = pipeline(Tasks.sentence_embedding, 
                       model=model_id)
    
    inputs = {
        "source_sentence": [query],
        "sentences_to_compare":paragraphs
    }
    
    result = pipeline_se(input=inputs)
    #sort the paragraphs according to the result['scores']
    scores = result['scores']
    paras = np.array(paragraphs)[np.array(scores).argsort()[::-1]][:topn2]
    
    model_id = 'damo/nlp_corom_passage-ranking_english-base'
    model = Model.from_pretrained(model_id)
    preprocessor = TextRankingTransformersPreprocessor(model.model_dir)
    pipeline_ins = pipeline(task=Tasks.text_ranking, model=model, preprocessor=preprocessor)
    inputs = {
         "source_sentence": [query],
         "sentences_to_compare":list(paras)
    }
    
    result = pipeline_ins(input=inputs)
    scores = result['scores']
    paras_new = np.array(paras)[np.array(scores).argsort()[::-1]]
    with open(f'{args.data_path}/rerank/{outline}_rerank.txt', 'w') as f:
        f.write('\n'.join(paras_new))
    
    print(f"rerank according to {query} finished, the rerank_data is saved in {args.data_path}/rerank/{outline}_rerank.txt")
    return paras_new
    
    


def rerank(args, paragraphs, query, keyword, outline, model_name='CoRoM', topn2=300):
    if model_name == 'CoROM':
        return CoROM(args, paragraphs, query, keyword,outline, topn2)
    else:
        raise NotImplementedError
    
if __name__ == '__main__':
    keyword = 'albert_einstein'
    outline = 'published_works'
    keyword_path = f'data/{keyword}/{outline}_retrieve.txt'
    with open(keyword_path, 'r') as f:
        paragraphs = f.read().split('\n')
    
    #query = 'how was the personal life of albert einstein'
    query = 'what published work did albert einstein have'
    paragraphs = list(filter(None, paragraphs))
    CoROM(paragraphs, query, keyword, outline)