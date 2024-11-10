import json
import os

class FileService:
    def __init__(self):
        # プロジェクトのルートディレクトリを取得
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    """
    ローカルファイルシステムからJSONファイルを読み取る
    :param path: ファイルが格納されているディレクトリのパス
    :param file_name: 読み込むファイル名
    :return: 読み込んだJSONコンテンツ
    """
    def read_json_from_file(self, path, file_name, encoding='utf-8'):
        file_path = ""
        try:
            # フルパスの生成
            file_path = os.path.join(self.root_dir, path, file_name)
            
            # ファイルを開いてJSONとしてパース
            with open(file_path, 'r', encoding=encoding) as file:
                contents = file.read()
                return json.loads(contents)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            raise
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {file_path}")
            raise
        except Exception as e:
            print(f"Error reading file: {e}")
            raise RuntimeError('Error reading JSON file')
        
    """
    JSONデータをローカルファイルシステムに書き込む
    :param data: 書き込むJSONデータ
    :param path: ファイルを保存するディレクトリのパス
    :param file_name: 保存するファイル名
    :param encoding: ファイルのエンコーディング（デフォルトはUTF-8）
    :param indent: JSONの整形時のインデント（デフォルトは4）
    """
    def write_json_to_file(self, data, path, file_name, encoding='utf-8', indent=4):
        try:
            # フルパスの生成
            file_path = os.path.join(self.root_dir, path, file_name)
            
            # ディレクトリが存在しない場合は作成
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # JSONデータをファイルに書き込む
            with open(file_path, 'w', encoding=encoding) as file:
                json.dump(data, file, ensure_ascii=False, indent=indent)
            
            print(f"JSON data successfully written to: {file_path}")
        except Exception as e:
            print(f"Error writing JSON to file: {e}")
            raise RuntimeError('Error writing JSON file')