from typing import Callable, Dict, Optional

from fastapi import APIRouter, BackgroundTasks, Body, Request, Response
from fastapi.routing import APIRoute
from starlette.background import BackgroundTask

from app import log
from app._types import Message, ReadSubscriptionsResponse, ReadTopicsResponse, TopicName
from app.const import PUBSUB_MAP
from app.subscriber import run_subscribers


class _APIRoute(APIRoute):
    """_APIRoute.

    _APIRoute is a custom APIRoute class that adds a background task to the
    response to log request and response data.
    """

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        def _log_info(req: Dict, res: Dict) -> None:
            log.info({"req": req})
            log.info({"res": res})

        async def custom_route_handler(request: Request) -> Response:
            # TODO: make nice pydantic types for req and res
            req = request.__dict__
            response = await original_route_handler(request)
            res = response.__dict__
            response.background.__dict__["tasks"].append(
                BackgroundTask(_log_info, req=req, res=res)
            )
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
async def publish_to_topic(bgt: BackgroundTasks, message: Message = Body(...)) -> None:
    log.info(f"Publishing message: {message.json()}")
    bgt.add_task(run_subscribers, message=message)
    log.info(f"Subscribers invoked for message: {message.json()}")
