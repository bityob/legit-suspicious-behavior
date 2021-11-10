import os

from app.connectors.base import AbstractConnectorService


GITHUB_WEBHOOK_URL = os.environ("GITHUB_WEBHOOK_URL")


class GitHubConnectorService(AbstractConnectorService):
    def __init__(self, url: str = GITHUB_WEBHOOK_URL) -> None:
        super().__init__(url=url)

    
        