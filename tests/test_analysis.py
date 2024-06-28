import unittest
from src.analysis.entity_recognition import entity_recognition

class TestEntityRecognition(unittest.TestCase):
    def test_entity_recognition(self):
        input_text = "John Doe works at OpenAI in San Francisco."
        expected_output = {
            "PERSON": ["John Doe"],
            "ORG": ["OpenAI"],
            "GPE": ["San Francisco"],
            "DATE": []
        }
        self.assertEqual(entity_recognition(input_text), expected_output)

if __name__ == "__main__":
    unittest.main()
