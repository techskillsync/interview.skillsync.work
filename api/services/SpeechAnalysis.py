'''
This particular file runs sentiment analysis on the given text passed as arg in analyze_sentiment func
Just call analyze_sentiment Function and pass text arg
'''

from pydantic import BaseModel
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)
import torch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentResponse(BaseModel):
    sentiment: str
    score: float

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# tokenizer = AutoTokenizer.from_pretrained(
#     "nlptown/bert-base-multilingual-uncased-sentiment"
# )
# model = AutoModelForSequenceClassification.from_pretrained(
#     "nlptown/bert-base-multilingual-uncased-sentiment"
# ).to(device)

tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest").to(device)

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text using a pre-trained sentiment analysis model.

    This function tokenizes the input text and feeds it to a transformer-based sentiment
    analysis model. It returns the sentiment classification (negative, neutral, positive)
    and its associated confidence score.

    Args:
        text (str): The input text to analyze for sentiment.

    Returns:
        SentimentResponse: A Pydantic model containing the predicted sentiment (as a string)
        and the confidence score (as a float).

    Example:
        response = analyze_sentiment("I love this product!")
        print(response.sentiment)  # Output: "positive"
        print(response.score)      # Output: confidence score for the "positive" sentiment
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        output = model(**inputs).logits
        probabilities = torch.nn.functional.softmax(output, dim=1)
        sentiment_index = torch.argmax(probabilities).item()
        sentiment_score = torch.max(probabilities).item()
# this mapping is for bert
    # sentiment_map = [
    #     "very negative",
    #     "negative",
    #     "neutral",
    #     "positive",
    #     "very positive",
    # ]
    sentiment_map = ["negative", "neutral", "positive"]
    return SentimentResponse(
        sentiment=sentiment_map[sentiment_index], score=sentiment_score
    )