from app._types import SubscriptionName, TopicName

PUBSUB_MAP = {
    TopicName.messages.value: {
        SubscriptionName.messages_processor,
        SubscriptionName.messages_counter,
    }
}
