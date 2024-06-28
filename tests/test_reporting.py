import unittest
import pandas as pd
from src.report_generation.create_webinar_report import generate_insights

class TestCreateWebinarReport(unittest.TestCase):
    def test_generate_insights(self):
        data = {
            'Webinar': ['Webinar 1'],
            'Summary': ['This is a summary.'],
            'Topics': ['[["topic1", "topic2"]]'],
            'Sentiment Polarity': [0.5],
            'Sentiment Explanation': ['Positive sentiment.'],
            'Contextual Explanation': ['Optimistic view.']
        }
        df = pd.DataFrame(data)
        insights = generate_insights(df)
        self.assertIn("Webinar: Webinar 1", insights)
        self.assertIn("Leverage Positive Sentiment and Optimism:", insights)

if __name__ == "__main__":
    unittest.main()
