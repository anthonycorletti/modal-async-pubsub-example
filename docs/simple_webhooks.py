import modal

stub = modal.Stub()


@stub.webhook()
def f() -> str:
    return "Hello world!"


if __name__ == "__main__":
    stub.serve()
