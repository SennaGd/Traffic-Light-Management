# responsible for making sure the get endpoint has the right template
from pydantic import BaseModel

class Messages_List(BaseModel):
	messages:list[Get_Train_Message | Get_Light_Message]
	timestamp: str

class Get_Message_Contents(BaseModel):
	id:str
	state:str


class Get_Train_Message(BaseModel):
	message:Get_Message_Contents
	type:str

class Get_Light_Message(BaseModel):
	id: str | None = None	
	lightId: str | None = None
	message: Get_Message_Contents
	type: str


