# Wiki Generation Project - README

## Introduction
The Wiki Generation Project is an automated framework for generating encyclopedia-style documents. This project integrates open-domain information retrieval and question-answering models, utilizing the HLATR technology and ChatGPT-4 model. It aims to solve challenges in understanding and generating long texts, enhancing the accuracy of information retrieval and producing content-rich, well-structured, and factually accurate encyclopedia documents.

## Components
The project comprises several Python scripts, each fulfilling a specific role in the document generation process:

### 1. `main.py`
- **Description**: Serves as the entry point for the program. Coordinates the overall process of document generation.
- **Usage**: Executes other modules and orchestrates the document generation workflow.

### 2. `dataHelper.py`
- **Description**: Provides the `get_data` interface which returns a dictionary. The keys are titles, and the values are the sorted dataset related to these titles.

### 3. `craw_data.py`
- **Description**: Uses specified keywords and the number of pages to crawl content from Google, returning a list of related URLs.
  
### 4. `clean_data.py`
- **Description**: Cleans the crawled data by removing noise and irrelevant information, following the methods used in the C4 dataset.

### 5. `generative_structure.py`
- **Description**: Determines the template structure for the document based on the most frequently appearing titles in similar encyclopedia documents for a given category of keywords.

### 6. `retrieve.py`
- **Description**: Offers the `retrieve` interface that returns a list of results sorted based on the BM25 score.

### 7. `rerank.py`
- **Description**: Provides the `rerank` interface, using the HLATR model to further sort the results obtained from the `retrieve` function.

### 8. `generative_wiki.py`
- **Description**: Utilizes the data from `get_data` and the GPT-4 interface to generate the content of the encyclopedia document.

### 9. `config.py`
- **Description**: Contains various configuration parameters needed for the program's operation.

### 10. `eval`
- **Description**: Responsible for automated evaluations, including TTR (Type-Token Ratio) assessment and LDA model evaluation.

## Configuration Parameters
The project offers several configurable parameters to tailor its operation to specific needs:

- **keyword**: The keyword for which the document is generated.
- **page**: The number of Google content pages to crawl.
- **type**: The category of the keyword, e.g., "scientist", "university".
- **LLM**: The large language model used for content generation, default is GPT-4.
- **retrieve_model/rerank_model**: Models used for retrieving and reranking content.
- **badword_filepath**: Path to the file containing a list of bad words, based on the C4 dataset.
- **raw_urls/clean_data**: Paths to store crawled URLs and cleaned text data.
- **bad_words_ratio**: Threshold for discarding articles with a high proportion of bad words.
- **temp_path**: Path to store document templates.
- **topn1, topn2**: Number of texts considered during retrieval and reranking.

## Running the Project
To run the project for a specific keyword and a set number of pages, use the following command:

```bash
python main.py --keyword "YourKeyword" --page YourPageNumber --type "YourType"
```

Ensure to configure the parameters appropriately before running the script.