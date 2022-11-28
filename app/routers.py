from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Body

from app import log
from app._types import Message, ReadSubscriptionsResponse, ReadTopicsResponse, TopicName
from app.const import PUBSUB_MAP
from app.subscriber import run_subscribers

topics_router = APIRouter(tags=["topics"])
subscriptions_router = APIRouter(tags=["subscriptions"])


@topics_router.get("/topics", response_model=ReadTopicsResponse)
async def get_topics() -> ReadTopicsResponse:
    return ReadTopicsResponse()


@subscriptions_router.get("/subscriptions", response_model=ReadSubscriptionsResponse)
async def get_subscriptions(
    topic_name: Optional[str] = None,
) -> ReadSubscriptionsResponse:
    if topic_name is None:
        return ReadSubscriptionsResponse(subscriptions=PUBSUB_MAP)
    elif topic_name in list(TopicName):
        return ReadSubscriptionsResponse(
            subscriptions={topic_name: PUBSUB_MAP[topic_name]}
        )
    else:
        return ReadSubscriptionsResponse(subscriptions={topic_name: []})


@topics_router.post("/topics", response_model=None)
def publish_to_topic(bgt: BackgroundTasks, message: Message = Body(...)) -> None:
    log.info(f"Publishing message: {message.json()}")
    bgt.add_task(run_subscribers, message=message)
    log.info(f"Subscribers invoked for message: {message.json()}")
