from pydantic import BaseModel, Field

import time
        
# api classes
class Message(BaseModel):
	id: str | int | float | list | dict = "" 
	expectedArrival: str = ""# time
	postTime: int = Field(default_factory=lambda: int(time.time())) 

class Packet(BaseModel):
    type: str | None = None 
    message: Message

# all packets inside messages
class Str_Request(BaseModel):
	messages: list[Packet] 


another_packet = Packet(
    type="update",
    message=Message(id="MSG-999", expectedArrival="12:00 PM")
	)
