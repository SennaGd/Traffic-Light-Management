import time
from pydantic import BaseModel

# linked list class
class Node():
    def __init__(self, light_id=None, priority=None):
        self.light_id = light_id
        self.priority = priority
        self.next = None
        
        
# api classes
class Message(BaseModel):
    id: str | None = None
    expectedArrival: str | None = None  # time


class Packet(BaseModel):
    type: str | None = None
    message: Message | None = None


class Message(BaseModel):
    messages: list[Packet]
    timestamp: float = time.time()

