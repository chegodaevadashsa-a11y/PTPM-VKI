
from abc import ABC, abstractmethod


class ExternalService(ABC):
    @abstractmethod
    def send(self, message):
        pass


class MockExternalService(ExternalService):
    def __init__(self):
        self.sent_messages = []

    def send(self, message):
        self.sent_messages.append(message)
        return True
