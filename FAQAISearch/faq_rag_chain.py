import os
import pandas as pd
from dotenv import load_dotenv
import numpy as np
import pickle

from vector_encoders import VertexAI
from faiss_indexer import FaissModel, FaissIndexer
from gemini_llm import GeminiLLM

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def build_index(vertexai, save_path):
    df = pd.read_csv('./data/faq.csv')
    vectors = []
    text_list = []
    for i, row in df.iterrows():
        q = row['question']
        a = row['answer']
        text = f"ID: {i} 質問: {q} 回答: {a}"
        v = vertexai.vectorize(text)
        v = v.astype("float32")
        vectors.append(v)
        text_list.append(text)
        print(i, text)
    dimension = len(vectors[0])
    vectors = np.array(vectors)
    indexer = FaissIndexer(FaissModel.COSINE, dimension)
    indexer.add2index(vectors)
    save_binary([indexer, text_list], save_path)
    return indexer, text_list

def save_binary(data, filepath):
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)
        
def load_binary(filepath):
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    return data

def rag_query(question):
    load_dotenv('./secrets/.env')
    vertexai = VertexAI(os.getenv('PROJECT_ID'), os.getenv('CREDENTIAL_FILE'), os.getenv('REGION'))
    #build_index(vertexai, './data/rag_indexer.pkl')
    [indexer, text_list] = load_binary('./data/rag_indexer.pkl')
    
    #question = "バッテリの修理はどれくらいかかりますか？"
    vector = vertexai.vectorize(question)
    numbers, scores = indexer.search(vector)
    candidates = ""
    for num, score in zip(numbers, scores):
        print(num, score, text_list[num])
        candidates += text_list[num] + '\r\n'
        
    llm = GeminiLLM(os.getenv('API_KEY'))
    prompt = "あなたはヘルプセンターで質問の対応をしています。次の質問にこたえなさい。\r\n"
    prompt += "質問：" + question + "\r\n\r\n"
    prompt += "以下が質問の候補です。\r\n"
    prompt += candidates
    prompt += "\r\n最も適切な回答とIDおよびその理由をJSON形式で出力してください。"
    ans = llm.query(prompt)
    return ans
    
if __name__ == '__main__':
    ans = rag_query('バッテリの修理にはどれくらいかかりますか？')
    print(ans)