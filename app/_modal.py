import modal
from fastapi import FastAPI

from app.main import api

stub = modal.Stub()


@stub.asgi()
def _api() -> FastAPI:
    return api


if __name__ == "__main__":
    stub.serve()
