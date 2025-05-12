import os
from deep_translator import GoogleTranslator
import pandas as pd
from tqdm import tqdm
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from time import sleep


def translate(text):
    trans = GoogleTranslator(source='auto', target="ja")
    trans_ja = trans.translate(text)
    return trans_ja

# https://www.kaggle.com/datasets/sunilthite/text-document-classification-dataset
df = pd.read_csv("help-desk-faq.csv")
#df = df[:10]


qs = df['Question'].to_list()
ans = df['Answer'].to_list()



result = []
for i, (q, a) in enumerate(zip(qs, ans)):
    if i >= 10 and i < 20:
        #    continue
        jq = translate(q)
        sleep(5)
        ja = translate(a)
        sleep(5)
        print(jq, ja)
        result.append([jq, ja])
  
df2 = pd.DataFrame(data=result, columns=['question', 'answer'])
df2.to_csv('faq2.csv', index=False)
#df2.to_csv("faq_ja.csv", index=False)



