from openai import OpenAI
from scipy.spatial.distance import cosine

class OpenAiService:
    def __init__(self, api_key):
        self.client = OpenAI()

    """
    ユーザーの質問に基づいて回答を生成するメソッド
    :param user_message: ユーザーが送信した質問やメッセージ
    :return: OpenAI の応答として生成された回答
    """
    def generate_answer(self, user_message):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "丁寧に回答してください。"},
                {"role": "user", "content": f"ユーザーからの質問: {user_message}"}
            ],
            max_tokens=500,
            temperature=0.5,
        )
        return response.choices[0].message.content

    """
    QAデータ（質問と回答のペア）を埋め込み（ベクトル形式）に変換するメソッド
    :param qa_data: 質問と回答のペアのリスト。各要素は { question, answer } の辞書。
    :return: 埋め込みデータを含むリスト。各質問が埋め込みベクトルとともに保存される。
    """
    def generate_embeddings(self, qa_data):
        embeddings = []

        for item in qa_data:
            question = item['question']
            answer = item['answer']

            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=question
            )

            embeddings.append({
                'question': question,
                'answer': answer,
                'embedding': response.data.embedding
            })

        return embeddings

    """
    ユーザーの質問に対して最も類似度の高い埋め込みを見つけるメソッド
    :param user_message: ユーザーからのメッセージ
    :param embeddings: 事前に生成された埋め込みデータのリスト
    :param similarity_threshold: コサイン類似度の閾値
    :return: 最も類似した質問に対する回答
    """
    def find_best_answer(self, user_message, embeddings, similarity_threshold=0.85):
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=user_message
        )
        user_embedding = response.data[0].embedding
        best_match = None
        highest_similarity = -1
        for item in embeddings:
            sim = 1 - cosine(user_embedding, item['embedding'])  # コサイン類似度の計算

            if sim > similarity_threshold and sim > highest_similarity:
                highest_similarity = sim
                best_match = item

        if best_match:
            return best_match['answer']
        else:
            return "当連盟以外の質問については回答することはできません。"