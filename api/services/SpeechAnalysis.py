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

bert_tokenizer = AutoTokenizer.from_pretrained(
    "nlptown/bert-base-multilingual-uncased-sentiment"
)
bert_model = AutoModelForSequenceClassification.from_pretrained(
    "nlptown/bert-base-multilingual-uncased-sentiment"
).to(device)

def analyze_sentiment(text):
    inputs = bert_tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        output = bert_model(**inputs).logits
        probabilities = torch.nn.functional.softmax(output, dim=1)
        sentiment_index = torch.argmax(probabilities).item()
        sentiment_score = torch.max(probabilities).item()

    sentiment_map = [
        "very negative",
        "negative",
        "neutral",
        "positive",
        "very positive",
    ]
    return SentimentResponse(
        sentiment=sentiment_map[sentiment_index], score=sentiment_score
    )