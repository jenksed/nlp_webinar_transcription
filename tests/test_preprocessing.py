import unittest
from src.preprocessing.preprocess_text import preprocess_text

class TestPreprocessText(unittest.TestCase):
    def test_preprocess_text(self):
        input_text = "This is a sample text, with punctuation!"
        expected_output = "sample text punctuation"
        self.assertEqual(preprocess_text(input_text), expected_output)

if __name__ == "__main__":
    unittest.main()
