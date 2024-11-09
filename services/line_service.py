import hmac
import hashlib
import base64
import urllib.request
import json
from urllib.error import HTTPError, URLError

class LineService:
    def __init__(self, channel_secret, access_token):
        self.channel_secret = channel_secret
        self.access_token = access_token

    """
    LINEから送られてきたリクエストの署名を検証するメソッド
    :param body: リクエストのボディ (文字列またはバイナリ形式)
    :param signature: リクエストヘッダーから取得した署名
    :return: 署名が正しい場合は True、それ以外は False
    """
    def validate_signature(self, body, signature):
        # HMAC-SHA256アルゴリズムを使用して署名を生成
        hash = hmac.new(
            self.channel_secret.encode('utf-8'),  # channel_secretをUTF-8にエンコード
            body.encode('utf-8'),  # リクエストボディをUTF-8にエンコード
            hashlib.sha256
        ).digest()

        # Base64形式でハッシュを取得
        computed_signature = base64.b64encode(hash).decode('utf-8')

        # 生成したハッシュと送られてきた署名を比較して、一致するか確認
        return computed_signature == signature

    """
    LINEに返信メッセージを送信するメソッド
    :param reply_token: LINEから送信された返信トークン
    :param message: ユーザーに送信するテキストメッセージ
    :return: メッセージ送信が成功または失敗するHTTPレスポンス
    """
    def send_reply_to_line(self, reply_token, message):
        reply_message = {
            "replyToken": reply_token,
            "messages": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }

        # LINEのAPIにリクエストを送信
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        url = 'https://api.line.me/v2/bot/message/reply'
        data = json.dumps(reply_message).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')

        try:
            with urllib.request.urlopen(req) as response:
                response_body = response.read()
                response_code = response.getcode()

            # エラーチェック
            if response_code != 200:
                raise Exception(f"Error sending message: {response_body.decode('utf-8')}")
            
            return {
                'status_code': response_code,
                'body': response_body.decode('utf-8')
            }

        except HTTPError as e:
            raise Exception(f"HTTP error occurred: {e.code} - {e.read().decode('utf-8')}")
        except URLError as e:
            raise Exception(f"URL error occurred: {e.reason}")