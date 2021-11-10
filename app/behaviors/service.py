import time

import redis

from app.behaviors.base import BehaviorMeta, RedisMessage
from app.connectors.github import GitHubConnectorService
from app.notifications.base import ConsoleNotification
from app.settings import REDIS_HOST, REDIS_PORT, EVENTS_CHANNEL_PATTERN, SOURCE_SERVICE_NAME


redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
connectors = {
    "github": GitHubConnectorService,
}


def main():
    p = redis_client.pubsub()
    
    events_channel = EVENTS_CHANNEL_PATTERN.format(service_name=SOURCE_SERVICE_NAME)
    
    p.subscribe(events_channel)

    connector_cls = connectors[SOURCE_SERVICE_NAME]

    while True:
        message = RedisMessage(p.get_message())
        
        if not message.data or message.type == "subscribe":
            time.sleep(1)
            continue

        event = connector_cls(event=message.data).to_event()

        print(f"event_type={event.event_type}")

        # Iterate over all behaviors and check for match
        for behavior_cls in BehaviorMeta.behaviors_dict.values():
            match = behavior_cls.match(event)
            print(f"behavior_cls={behavior_cls}, match={match}")

            if match:
                ConsoleNotification(
                    message=f"********\nFound suspicious behavior\nBehavior: {behavior_cls.__name__}\n*********"
                ).notify()

        time.sleep(1)


if __name__ == '__main__':
    main()