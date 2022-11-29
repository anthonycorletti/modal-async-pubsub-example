import modal
from fastapi import FastAPI

from app._env import env
from app.main import api

stub = modal.Stub()

stub["env"] = modal.Secret(env.dict())

image = modal.Image.debian_slim().pip_install(
    [
        "fastapi >=0.70.0",
        "python-dotenv >=0.21.0",
        "structlog >=21.2.0",
    ]
)


@stub.asgi(image=image, secret=stub["env"])
def _api() -> FastAPI:
    return api


if __name__ == "__main__":
    stub.serve()
