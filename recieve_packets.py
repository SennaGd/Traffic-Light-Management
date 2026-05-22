from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from structs.get_state import *
from structs.packets import Str_Request 
from structs.post_state import Post_Str_Request
from json_variables import insertIntoPacketsList, fetchLightStates

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# post is only for WRITING to packets.json
@app.post("/post")
async def recieve(requests: Str_Request):
	messages = requests.messages
	for packet in messages:
		print("retrieved:", packet)
		insertIntoPacketsList(packet)
	return "hlelow" 

@app.get("/state")
async def fetchStates():
	lightStates = fetchLightStates()
	messages = Messages_List(messages=[], timestamp="")


	for light in lightStates:

		# traffic lights

		
		if light != "train-1":
			lightID = light

			light_object = Get_Light_Message(
					message=Get_Message_Contents(id=str(lightID), state='green'), 
					type='trafficLightState', lightId=str(lightID), id=str(lightID)) 
				
		elif light == "train-1":
			light_object = Get_Train_Message(
					message=Get_Message_Contents(id='rail-1', state='opening'), 
					type='crossingGate') 
				
		messages.messages.append(light_object) # append the state :P
	print(messages)

	from datetime import datetime

# 1. The exact format string for your example:
	date_format = "%Y-%m-%dT%H:%M:%SZ"

# 2. How to format the current time right now:
	current_time_str = datetime.now().strftime(date_format)
	print(current_time_str)	
	messages.timestamp = current_time_str
	return messages  
