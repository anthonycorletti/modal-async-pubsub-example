import asyncio

from app import env, log
from app._types import Message, SubscriptionName


async def run_subscriber(subscriber_name: SubscriptionName, message: Message) -> None:
    log.info(f"Running subscriber {subscriber_name.value}")
    log.info(f"Processing message: {message.json()}")
    # secret = modal.Secret.from_name("my-custom-secret")
    log.info(f"Secret value: {env.API_SECRET_KEY}")
    # log.info(f"hey its a secret: {os.environ['API_SECRET_KEY']}")
    await asyncio.sleep(2)
    log.info(f"Finished processing message: {message.json()}")
