import os
import sys
sys.path.append(os.getcwd())

from dotenv import load_dotenv
load_dotenv()

from services.file_service import FileService
from services.local_llm_service import LocalLlmService
import unittest

class LocalLlmServiceTest(unittest.TestCase):
    def test_embeddings(self):
        fileService = FileService()
        qa = fileService.read_json_from_file("Data", "qa.json")
        localLlmService = LocalLlmService()
        embeddings = localLlmService.generate_embeddings(qa)
        fileService.write_json_to_file(embeddings, "Data", "qaembedding.json")

if __name__ == '__main__':
    unittest.main()