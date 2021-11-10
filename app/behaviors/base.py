from datetime import datetime
import json
from typing import Optional

from app.connectors.base import Event
from app.settings import DATETIME_FORMAT


class BehaviorMeta(type):
    behaviors_dict = {}

    def __new__(cls, name, bases, dct):
        curr_cls = super().__new__(cls, name, bases, dct)

        cls.behaviors_dict[name] = curr_cls

        return curr_cls


class AbstractBehavior:
    event_type = None

    @classmethod
    def match(cls, event: Event) -> bool:
        raise NotImplementedError()


class TeamWithHackerPrefixBehavior(AbstractBehavior, metaclass=BehaviorMeta):
    event_type = "team_created"
    team_name_prefix = "hacker"

    @classmethod
    def match(cls, event: Event) -> bool:
        if event.event_type != cls.event_type:
            return False

        team_name: str = event.data["team"]["name"]

        return team_name.startswith(cls.team_name_prefix)


class PushCodeInAfterNoonBehavior(AbstractBehavior, metaclass=BehaviorMeta):
    event_type = "push"
    begin_hour = 14
    end_hour = 15

    @classmethod
    def match(cls, event: Event) -> bool:
        if event.event_type != cls.event_type:
            return False
        
        # We don't use the head commit timestamp because the push can be later than the commit itself
        # unless the PR is squashed and a new commit is just created
        # therefore we use the time now because events are pushed on realtime

        # We don't use "pushed_at" too
        # Because it's beeing updated by any of the branches 
        # (not for sure the one the triggered now the event)
        # See: https://stackoverflow.com/a/15922637

        datetime_obj = datetime.utcnow()

        print(datetime_obj.hour)

        # match if time is between 14:00 <= now < 16:00
        return cls.begin_hour <= datetime_obj.hour <= cls.end_hour

class RepositoryDeletedIn10MinutesFromCreationBehavior(AbstractBehavior, metaclass=BehaviorMeta):
    event_type = "repository_deleted"

    @classmethod
    def match(cls, event: Event) -> bool:
        if event.event_type != cls.event_type:
            return False

        created_time = datetime.strptime(
            event.data["repository"]["created_at"],
            DATETIME_FORMAT,
        )

        print(f"created_time={created_time}")

        now = datetime.utcnow()

        print(f"now={now}")

        # Return true if there are less than 10 minutes between creation and deletion
        # the delta here doesn't have `minutes` attribute, therefore we use the seconds instead
        return (now - created_time).total_seconds() < 10 * 60
          

class RedisMessage:
    type = None
    channel = None
    data = None

    def __init__(self, data: Optional[dict]):
        if not data:
            return

        self.type = data["type"]
        self.channel = data["channel"]
        self.data = data["data"]

        try:
            # Try to load as json
            self.data = json.loads(self.data)
        except:
            pass