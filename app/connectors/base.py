from dataclasses import dataclass


@dataclass
class Event:
    event_type: str
    data: dict


class BaseConnectorService:
    def __init__(self, event: dict) -> None:
        self.event = event
        self.event_type = self.get_event_type(event)

    def get_event_type(self, event) -> str:
        action = self.get_action_field()
        event_field = self.get_event_field()

        if action:
            return f"{event_field}_{action}"

        return event_field

    def get_event_field(self) -> str:
        raise NotImplementedError()

    def get_action_field(self) -> str:
        raise NotImplementedError()

    def to_event(self) -> Event:
        return Event(
            event_type=self.event_type,
            data=self.event,
        )

