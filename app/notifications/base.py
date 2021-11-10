class AbstractNotification:
    def __init__(self, message: str):
        self.message = message

    def notify(self):
        raise NotImplementedError()


class ConsoleNotification(AbstractNotification):
    def notify(self):
        print(f"Notification: {self.message}")