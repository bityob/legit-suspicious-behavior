import os

from app.connectors.base import BaseConnectorService


class GitHubConnectorService(BaseConnectorService):
    def get_event_field(self) -> str:
        return self.event["event_type"]

    def get_action_field(self) -> str:
        return self.event.get("action") or ""

    
        