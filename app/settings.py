import os


EVENTS_TABLE_PATTERN = "{service_name}_events"
EVENTS_CHANNEL_PATTERN = "events/{service_name}"

MONGO_HOST = "localhost"
MONGO_PORT = 27017

REDIS_HOST = "localhost"
REDIS_PORT = 6379

SOURCE_SERVICE_NAME = os.getenv("SOURCE_SERVICE_NAME", "github")

# 2021-11-10T15:58:39Z
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"