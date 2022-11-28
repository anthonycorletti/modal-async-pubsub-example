from enum import Enum, unique
from typing import Dict, List

from pydantic import BaseModel


@unique
class TopicName(str, Enum):
    messages = "messages"


class ReadTopicsResponse(BaseModel):
    topics: List[TopicName] = list(TopicName)


@unique
class SubscriptionName(str, Enum):
    messages_processor = "messages_processor"
    messages_counter = "messages_counter"


class ReadSubscriptionsResponse(BaseModel):
    subscriptions: Dict[str, List[SubscriptionName]]


class Message(BaseModel):
    topic: TopicName
    data: bytes

    class Config:
        schema_extra = {
            "example": {
                "topic": TopicName.messages,
                "data": b"Hello world!",
            }
        }


class SubscriberResponse(BaseModel):
    name: SubscriptionName
    message: Message
