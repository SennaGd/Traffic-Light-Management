from pydantic import BaseModel, Field

        
# api classes
class PMessage(BaseModel):
	id: str = ""
	state: str = "red" # default state: red
	
class PostState(BaseModel):
    type: str = Field(default="TrafficLightState")
    message: PMessage

# all packets inside messages
class Post_Str_Request(BaseModel):
	messages: list[PostState] 


another_packet = PostState(
    message=PMessage(
		id="8.1",
		state="green"
	)
)

