import modal
from fastapi import FastAPI

from app._env import env
from app.main import api

stub = modal.Stub()

stub["env"] = modal.Secret(env.dict())


@stub.asgi(secret=stub["env"])
def _api() -> FastAPI:
    return api


if __name__ == "__main__":
    stub.serve()
