from typing import Callable, Optional

from fastapi import APIRouter, BackgroundTasks, Body, Request, Response
from fastapi.routing import APIRoute

from app import log
from app._types import (
    Message,
    ReadSubscriptionsResponse,
    ReadTopicsResponse,
    RequestLoggerMessage,
    ResponseLoggerMessage,
    TopicName,
)
from app.const import PUBSUB_MAP
from app.subscriber import run_subscribers


class _APIRoute(APIRoute):
    """_APIRoute.

    _APIRoute is a custom APIRoute class that adds a background task to the
    response to log request and response data.
    """

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        def _log(req: RequestLoggerMessage, res: ResponseLoggerMessage) -> None:
            log.info({"req": req.dict()})
            log.info({"res": res.dict()})

        async def custom_route_handler(request: Request) -> Response:
            req = RequestLoggerMessage(**request.__dict__)
            response = await original_route_handler(request)
            res = ResponseLoggerMessage(**response.__dict__)
            _log(req=req, res=res)
            return response

        return custom_route_handler


topics_router = APIRouter(
    route_class=_APIRoute,
    tags=["topics"],
)

subscriptions_router = APIRouter(
    route_class=_APIRoute,
    tags=["subscriptions"],
)


@topics_router.get("/topics", response_model=ReadTopicsResponse)
async def get_topics() -> ReadTopicsResponse:
    """Get topics."""
    return ReadTopicsResponse()


@subscriptions_router.get("/subscriptions", response_model=ReadSubscriptionsResponse)
async def get_subscriptions(
    topic_name: Optional[str] = None,
) -> ReadSubscriptionsResponse:
    """Get subscriptions.

    Args:
        topic_name (Optional[str], optional): The topic name. Defaults to None.

    Returns:
        ReadSubscriptionsResponse: The response.
    """
    if topic_name is None:
        return ReadSubscriptionsResponse(subscriptions=PUBSUB_MAP)
    elif topic_name in list(TopicName):
        return ReadSubscriptionsResponse(
            subscriptions={topic_name: PUBSUB_MAP[topic_name]}
        )
    else:
        return ReadSubscriptionsResponse(subscriptions={topic_name: []})


@topics_router.post("/topics", response_model=None)
async def publish_to_topic(bgt: BackgroundTasks, message: Message = Body(...)) -> None:
    """publish_to_topic.

    Args:
        bgt (BackgroundTasks): Background tasks. This is used to run the subscribers.
        message (Message): Message to publish. This is the body of the request.

    Returns:
        None.
    """
    log.info(f"Publishing message: {message.json()}")
    bgt.add_task(run_subscribers, message=message)
    log.info(f"Subscribers invoked for message: {message.json()}")
