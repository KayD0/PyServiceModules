import boto3
import json
import logging
from botocore.exceptions import ClientError

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        # Amazon S3クライアントの初期化
        # 認証情報を明示的に指定
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)

    """
    Amazon S3からJSONファイルを読み取る
    :param bucket_name: S3バケット名
    :param path: ファイルが格納されているディレクトリのパス
    :param file_name: 読み込むファイル名
    :return: 読み込んだJSONコンテンツ
    """
    def read_json_from_file(self, bucket_name, path, file_name):
        try:
            full_path = f"{path}/{file_name}"
            
            response = self.s3_client.get_object(Bucket=bucket_name, Key=full_path)
            
            if 'Body' not in response:
                raise KeyError("'Body' not found in response")
        
            body = response['Body']
            if not hasattr(body, 'read'):
                raise AttributeError(f"'Body' object has no attribute 'read'. Type: {type(body)}")
            
            contents = body.read()
            if not isinstance(contents, (str, bytes)):
                raise TypeError(f"Unexpected content type: {type(contents)}")
            
            if isinstance(contents, bytes):
                contents = contents.decode('utf-8')
            
            # JSONとしてパース
            return json.loads(contents)
        except ClientError as e:
            raise RuntimeError(f'Error reading JSON file: {e}')
        except json.JSONDecodeError as e:
            raise RuntimeError(f'Error decoding JSON file: {e}')
        except Exception as e:
            raise RuntimeError(f'Unexpected error while reading file: {e}')