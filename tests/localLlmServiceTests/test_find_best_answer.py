import os
import sys
sys.path.append(os.getcwd())

from dotenv import load_dotenv
load_dotenv()

from services.file_service import FileService
from services.local_llm_service import LocalLlmService
import unittest

class LocalLlmServiceTest(unittest.TestCase):
    def test_find_answer(self):
        user_message = "会社の設立"
        file_path = "Data"
        file_name = "qaembedding.json"
        
        fileService = FileService()
        embeddings = fileService.read_json_from_file(file_path, file_name)
        
        localLlmService = LocalLlmService()
        localLlmService.add_embeddings(embeddings)
        
        ai_response = localLlmService.find_best_answer(user_message)
        print(ai_response)

if __name__ == '__main__':
    unittest.main()