
from math import log
import operator
import os
from tqdm import tqdm
import nltk
from nltk.stem import PorterStemmer
import re
stemmer = PorterStemmer()

# 下载词干化器所需的数据
nltk.download('punkt')
from config import parse_args

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0

def process_text(text):
    # 使用正则表达式删除标点符号和数字
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # 将文本分成单词
    words = text.split()
    
    # 对每个单词进行词干化并保留词根
    stemmed_words = [stemmer.stem(word) for word in words]
    
    # 将词干化后的单词重新组合成字符串
    processed_text = ' '.join(stemmed_words)
    
    return processed_text

class InvertedIndex:

	def __init__(self):
		self.index = dict()

	def __contains__(self, item):
		return item in self.index

	def __getitem__(self, item):
		return self.index[item]

	def add(self, word, docid):
		if word in self.index:
			if docid in self.index[word]:
				self.index[word][docid] += 1
			else:
				self.index[word][docid] = 1
		else:
			d = dict()
			d[docid] = 1
			self.index[word] = d

	#frequency of word in document
	def get_document_frequency(self, word, docid):
		if word in self.index:
			if docid in self.index[word]:
				return self.index[word][docid]
			else:
				raise LookupError('%s not in document %s' % (str(word), str(docid)))
		else:
			raise LookupError('%s not in index' % str(word))

	#frequency of word in index, i.e. number of documents that contain word
	def get_index_frequency(self, word):
		if word in self.index:
			return len(self.index[word])
		else:
			raise LookupError('%s not in index' % word)


class DocumentLengthTable:

	def __init__(self):
		self.table = dict()

	def __len__(self):
		return len(self.table)

	def add(self, docid, length):
		self.table[docid] = length

	def get_length(self, docid):
		if docid in self.table:
			return self.table[docid]
		else:
			raise LookupError('%s not found in table' % str(docid))

	def get_average_length(self):
		sum = 0
		for length in self.table.values():
			sum += length
		return float(sum) / float(len(self.table))

class QueryProcessor:
	def __init__(self, queries, corpus):
		self.queries = queries
		self.index, self.dlt = build_data_structures(corpus)

	def run(self):
		results = []
		for query in self.queries:
			print(query)
			
			results.append(self.run_query(query))
		return results

	def run_query(self, query):
		query_result = dict()
		for term in query:
			if term in self.index:
				doc_dict = self.index[term] # retrieve index entry
				for docid, freq in doc_dict.items(): #for each document and its word frequency
					score = score_BM25(n=len(doc_dict), f=freq, qf=1, r=0, N=len(self.dlt),
									   dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length()) # calculate score
					if docid in query_result: #this document has already been scored once
						query_result[docid] += score
					else:
						query_result[docid] = score
		return query_result


def build_data_structures(corpus):
	idx = InvertedIndex()
	dlt = DocumentLengthTable()
	for docid in corpus:

		#build inverted index
		for word in corpus[docid]:

			#delete the number and punctuation in word 
			idx.add(str(word), str(docid))

		#build document length table
		length = len(corpus[str(docid)])
		dlt.add(docid, length)
	return idx, dlt

def score_BM25(n, f, qf, r, N, dl, avdl):
	K = compute_K(dl, avdl)
	first = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
	second = ((k1 + 1) * f) / (K + f)
	third = ((k2+1) * qf) / (k2 + qf)
	return first * second * third


def compute_K(dl, avdl):
	return k1 * ((1-b) + b * (float(dl)/float(avdl)) )


def BM25(args, docs, query, topn1):
    
    
    query = [list(map(stemmer.stem, q)) for q in query]
    keyword_key = args.keyword.lower().replace(' ', '_')
    if not os.path.exists(f'{args.data_path}/{keyword_key}_clean_stem.txt'):
        stemmer_docs = list(map(process_text, docs))
        with open(f'{args.data_path}/{keyword_key}_clean_stem.txt', 'w') as f:
            f.write('\n'.join(stemmer_docs))
    else:
        with open(f'{args.data_path}/{keyword_key}_clean_stem.txt', 'r') as f:
            stemmer_docs = f.read().split('\n')
    docs = {str(i):doc.split(' ') for i, doc in enumerate(docs)}

    stemmer_docs = {str(i):doc.split(' ') for i, doc in enumerate(stemmer_docs)}
    proc = QueryProcessor(query, stemmer_docs)
    results = proc.run()
    qid = 0
    retrieve_results = []
    for result in results:
        sorted_x = sorted(result.items(), key=operator.itemgetter(1))
        sorted_x.reverse()
        index = 0
        for i in sorted_x[:topn1]:
            tmp = (qid, i[0], index, i[1])
            print('{:>1}\t{:>4}\t{:>2}\t{:>12}\tNH-BM25'.format(*tmp))
            retrieve_results.append(docs[i[0]])
            index += 1
            
        qid += 1
    
    # return the top 100 documents
    retrieve_results = [' '.join(result) for result in retrieve_results]
    return retrieve_results
        

def retrieve(args, docs, query, retrieve_model, topn1):

    if retrieve_model == 'BM25':
        return BM25(args, docs, query, topn1)
    raise NotImplementedError


if __name__ == '__main__':
    args = parse_args()
    keyword_key = args.keyword.lower().replace(' ', '_')
    args.data_path = os.path.join(args.data_path, keyword_key)
    with open(f'{args.data_path}/{keyword_key}_clean.txt', 'r') as f:
        docs = f.read().split('\n')
    
    
    if not os.path.exists(f'{args.data_path}/{keyword_key}_clean_stem.txt'):
        stemmer_docs = list(filter(None, map(process_text, docs)))
        with open(f'{args.data_path}/{keyword_key}_clean_stem.txt', 'w') as f:
            f.write('\n'.join(stemmer_docs))
        
            
    