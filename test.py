import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings
from nltk.sentiment import SentimentIntensityAnalyzer
from demo_test import classify_sentiment, main  # Import functions from your app

@pytest.fixture
def sample_comments():
    # Mocked sample comments for testing
    return [
        {'body': 'This is a positive comment.', 'created_utc': datetime.now().timestamp() - 3600},  # 1 hour ago
        {'body': 'This is a negative comment.', 'created_utc': datetime.now().timestamp() - 86400},  # 1 day ago
        {'body': 'This is a neutral comment.', 'created_utc': datetime.now().timestamp() - 604800}  # 1 week ago
    ]

def test_classify_sentiment():
    # Test sentiment classification based on polarity score
    assert classify_sentiment(0.05) == 'Positive'
    assert classify_sentiment(-0.05) == 'Negative'
    assert classify_sentiment(0.0) == 'Neutral'


