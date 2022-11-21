from fastapi import FastAPI

from app import __version__
from app.routers import pubsub_router, subscriptions_router, topics_router

api = FastAPI(title="modal-async-pubsub-api", version=__version__)

api.include_router(topics_router)
api.include_router(subscriptions_router)
api.include_router(pubsub_router)
