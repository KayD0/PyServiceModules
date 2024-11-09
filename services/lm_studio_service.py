# Make sure to `pip install openai` first
from openai import OpenAI

# ローカルのLlama modelを使用するためのカスタム埋め込みクラス
class LocalLlamaEmbedding():
    def __init__(self, api_url):
        self.client = OpenAI(base_url=api_url, api_key="lm-studio")

    def get_embedding(self, text, model="text-embedding-multilingual-e5-large-instruct"):
        return self.client.embeddings.create(input = [text], model=model).data[0].embedding
    
    def get_answer(self, text, model="llama-3.2-1b-instruct"):
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Always answer in rhymes."},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message