import os
import numpy as np
from vertexai.language_models import TextEmbeddingModel
import vertexai
from google.oauth2 import service_account

os.chdir(os.path.dirname(os.path.abspath(__file__)))

MODEL = {'name':'text-multilingual-embedding-002', 'token_max': 12800}

class VertexAI:
    def __init__(self, project_id, credential_json, location):
        #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_json
        credentials = service_account.Credentials.from_service_account_file(credential_json)
        vertexai.init(project=project_id, location=location, credentials=credentials)

    def vectorize(self, text, embedding_model=MODEL):
        model = TextEmbeddingModel.from_pretrained(embedding_model['name'])
        count = model.count_tokens(text)
        if count.total_tokens > embedding_model['token_max']:
            return None
        embeddings = model.get_embeddings([text])
        vector = embeddings[0].values
        return np.array(vector)
        
def test():
    PROJECT_ID = 'my-vertexai-459306'
    CREDENTIAL_FILE = 'my-vertexai-459306-293f0db3db5d.json'
    API_KEY = 'AIzaSyCcfXAFvTcbYTlCAZfYSSpGbzlJIzYpn3k'
    vertexai = VertexAI(PROJECT_ID, CREDENTIAL_FILE, "us-central1")
    vector = vertexai.vectorize("こんにちは")
    print(len(vector))
    
if __name__ == "__main__":
    test()