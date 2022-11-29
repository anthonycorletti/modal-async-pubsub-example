import modal
from fastapi import FastAPI

from app._env import env
from app.main import api

stub = modal.Stub()


def _set_secrets_in_modal() -> None:
    modal.Secret(env.dict())


@stub.asgi()
def _api() -> FastAPI:
    return api


if __name__ == "__main__":
    _set_secrets_in_modal()
    stub.serve()
