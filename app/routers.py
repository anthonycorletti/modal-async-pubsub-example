import asyncio

from fastapi import APIRouter, Body

from app import log
from app._types import (
    PUBSUB_MAP,
    Message,
    PubsubResponse,
    ReadSubscriptionsResponse,
    ReadTopicsResponse,
)
from app.subscriber import run_subscriber

topics_router = APIRouter(tags=["topics"])
subscriptions_router = APIRouter(tags=["subscriptions"])
pubsub_router = APIRouter(tags=["pubsub"])


@topics_router.get("/topics", response_model=ReadTopicsResponse)
async def get_topics() -> ReadTopicsResponse:
    return ReadTopicsResponse()


@topics_router.post("/topics", response_model=None)
async def publish_to_topic(message: Message = Body(...)) -> None:
    log.info(f"Publishing message {message.json()}")
    await asyncio.gather(
        *[
            run_subscriber(subscriber_name=subscriber_name, message=message)
            for subscriber_name in PUBSUB_MAP[message.topic]
        ]
    )


@subscriptions_router.get("/subscriptions", response_model=ReadSubscriptionsResponse)
async def get_subscriptions() -> ReadSubscriptionsResponse:
    return ReadSubscriptionsResponse()


@pubsub_router.get("/pubsub", response_model=PubsubResponse)
async def get_pubsub() -> PubsubResponse:
    return PubsubResponse()
