from enum import Enum, unique
from typing import Dict, List, Set

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
    subscriptions: List[SubscriptionName] = list(SubscriptionName)


PUBSUB_MAP = {
    TopicName.messages: {
        SubscriptionName.messages_processor,
        SubscriptionName.messages_counter,
    }
}


class PubsubResponse(BaseModel):
    pubsub_map: Dict[TopicName, Set[SubscriptionName]] = PUBSUB_MAP


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
