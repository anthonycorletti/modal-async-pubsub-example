from enum import Enum, unique
from typing import Dict, List

from pydantic import BaseModel, Json, StrictInt, StrictStr


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


class Scope(BaseModel):
    type: StrictStr
    # asgi: Dict
    http_version: StrictStr
    method: StrictStr
    scheme: StrictStr
    # root_path: StrictStr
    path: StrictStr
    # raw_path: str
    headers: List
    query_string: bytes


class SubscriberResponse(BaseModel):
    name: SubscriptionName
    message: Message


class RequestLoggerMessage(BaseModel):
    scope: Scope
    _stream_consumed: bool
    _is_disconnected: bool


class ResponseLoggerMessage(BaseModel):
    status_code: StrictInt
    body: Json
    raw_headers: List
