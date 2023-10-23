
import random
from enum import Enum
from time import sleep


class Sentiment(str, Enum):
    POSITIVE = 'POSITIVE'
    NEGATIVE = 'NEGATIVE'
    NEUTRAL = 'NEUTRAL'


class Topic(str, Enum):
    PRICING = 'PRICING'
    PRODUCT_FEATURES = 'PRODUCT_FEATURES'
    CUSTOMER_SERVICE = 'CUSTOMER_SERVICE'
    OTHER = 'OTHER'


# Randomly assign a sentiment to the text
def _get_sentiment(_text: str):
    return random.choice(list(Sentiment))


# Randomly assign a topic to the text
def _get_topic(_text: str):
    return random.choice(list(Topic))


def process_feedback_impl(payload: dict):
    delay = random.randint(5, 10)
    sleep(delay)

    text = payload.get("feedback")
    return {
        "sentiment": _get_sentiment(text),
        "topic": _get_topic(text)
    }
