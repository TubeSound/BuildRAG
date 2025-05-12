import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiLLM:
    def __init__(self, apikey, model_name="gemini-2.5-flash-preview-04-17"):
        self.apikey = apikey    
        genai.configure(api_key=apikey)
        llm = genai.GenerativeModel(model_name)
        self.llm = llm

    def models_name(self):
        lis = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
               lis.append(m.name)
        return lis

    def query(self, prompt):
        response = self.llm.generate_content(prompt)
        return response.text
    
    
    
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv('.env')
    llm = GeminiLLM(os.getenv("API_KEY"))
    question = "日本で、美味しい魚料理を教えてください?"
    ans = llm.query(question)
    print(ans)