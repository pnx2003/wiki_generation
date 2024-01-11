import openai
import os

openai.api_key = "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"
def llm(prompt, model, stop=["\n"]):
    response = openai.Completion.create(
      model=model,
      prompt=prompt,
      temperature=0,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.0,
    )
    return response["choices"][0]["text"]


def extract(data, model, prompt, keyword, output_path):
    outline = prompt.lower().replace(' ', '_')
    prompt_new = f"""As a learning assistant with no prior knowledge of {keyword}, you have received some text fragments about the {prompt} of {keyword}. Your task is to synthesize these fragments and outline its {prompt}. Please use only the information provided and avoid adding any external knowledge. Please present the integrated information in a structured and coherent manner suitable for a Wikipedia entry."""
    prompt_new = '\n'.join(data[prompt])[:120000] + '\n' + prompt_new
    with open('./tmp/prompt.txt', 'w') as f:
        f.write(prompt_new)
    
    import pdb;pdb.set_trace()
    if model == 'GPT4-Turbo-128':
        pass
        
        # result = llm(prompt, model)
        
        # with open(f'{output_path}/{outline}.txt', 'w') as f:
        #     f.write(result)
    else:
        raise NotImplementedError
        

def generate_wiki(data, model, prompts, keyword, output_path):
    res = f'#{keyword}\n\n'
    for prompt in prompts:
        outline  = prompt.lower().replace(' ', '_')
        prompt_wikipath = f'{output_path}/{outline}.txt'
        if not os.path.exists(prompt_wikipath):
            extract(data, model, prompt, keyword, output_path)
        
        with open(prompt_wikipath, 'r') as f:
            res += '##' + prompt + '\n\n' + f.read() + '\n\n\n'
            
    with open (f'{output_path}/output.txt', 'w') as f:
        f.write(res)
    
    
if __name__ == '__main__':
    outline = 'published_works'
    keyword = 'Albert Einstein'
    keyword_key = keyword.lower().replace(' ','_')
    with open(f'./data_new/{keyword_key}/{outline}_rerank.txt', 'r') as f:
        data = f.read().split('\n')
    #extract(data[:80], '')
    with open(f'./data/{keyword_key}/{outline}_rerank_80.txt', 'w') as f:
        f.write('\n'.join(data[:15]))