from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, PromptTemplate
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.schema import Document

class LlamaService:
    def __init__(self):
        self.embed_model = OpenAIEmbedding()
        self.vector_store = SimpleVectorStore(stores_text=True)
        self.index = None
        # 会社のQAボット用のプロンプトテンプレートを定義
        self.qa_template = PromptTemplate(
            "以下は弊社に関する情報です：\n"
            "---------------------\n"
            "{context_str}"
            "\n---------------------\n"
            "この情報を踏まえて、以下の質問にお答えください：{query_str}\n"
            "回答の際は以下の点に注意してください：\n"
            "1. 弊社の広報担当者として丁寧かつ簡潔に回答してください。\n"
            "2. 回答は必ず完全な文章で行い、単語や数字だけの回答は避けてください。\n"
            "3. 会社に関する情報を提供する際は、「弊社」という言葉を使用してください。\n"
            "4. 提供された情報に基づいて回答し、情報がない場合は「申し訳ありませんが、その情報は持ち合わせておりません」と答えてください。\n"
            "5. 質問の意図が不明確な場合は、丁寧に確認を求めてください。\n"
            "それでは、質問にお答えください：\n"
        )


    """
    QAデータ（質問と回答のペア）を埋め込み（ベクトル形式）に変換するメソッド。
    :param qa_data: 質問と回答のペアのリスト。各要素は { question, answer } の辞書。
    :return: 埋め込みデータを含むリスト。各質問が埋め込みベクトルとともに保存される。
    """
    def generate_embeddings(self, qa_data):
        embeddings = []

        for item in qa_data:
            question = item['question']
            answer = item['answer']

            # 質問のベクトル化
            question_embedding = self.embed_model.get_text_embedding(
                question
            )

            embeddings.append({
                'question': question,
                'answer': answer,
                'embedding': question_embedding
            })

        return embeddings

    """
    埋め込みベクトルをインデックスに追加する
    :param embeddings: 追加する埋め込みベクトルのリスト。各要素は'answer'と'embedding'キーを持つ辞書
    :return: None
    """
    def add_embeddings(self, embeddings):
        # 各埋め込みベクトルをDocumentオブジェクトに変換
        docs = []
        for item in embeddings:
            doc = Document(
                text=item['answer'],
                extra_info={'question': item['question']},
                embedding=item['embedding']
            )
            docs.append(doc)
        
        # ベクトルストアにドキュメントを追加
        self.vector_store.add(docs)
        if self.index is None:
            # インデックスが未初期化の場合、新しいインデックスを作成
            storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
            self.index = VectorStoreIndex(
                docs,
                storage_context=storage_context
            )

    """
    ユーザーのメッセージに最も適した回答を見つける
    :param user_message: ユーザーからの質問メッセージ
    :param similarity_threshold: 類似度の閾値（デフォルト: 0.85）
    :return: 最適な回答または規定のメッセージ
    """
    def find_best_answer(self, user_message, similarity_threshold=0.85):
        # クエリエンジンを初期化（上位1件の結果を取得）
        query_engine = self.index.as_query_engine(
            text_qa_template= self.qa_template,
            similarity_top_k=1,
            vector_store_query_mode="default",
            max_tokens=500,
        )

        # ユーザーメッセージに対してクエリを実行
        response = query_engine.query(user_message)
        
        # 類似度が閾値を超える回答が見つかった場合はその回答を返す
        if response.source_nodes and response.source_nodes[0].score > similarity_threshold:
            return response.response
        else:
            return "当連盟以外の質問については回答することはできません。"