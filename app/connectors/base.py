class AbstractConnectorService:
    def __init__(self, url) -> None:
        self.url = url        
        
    def get_events(self):
        raise NotImplementedError()