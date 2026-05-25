# responsible for checking if there's a train coming | calculating time to shutdown lights for train
from json_variables import *
from toggle_light import *
from select_group import findGroups
import time

packetsList = updatePacketsList()

def checkForTrain() -> bool:	
	trainComing = False
	for packet in packetsList:

		if packet[1] == "train-1":
			trainComing = True		

	return trainComing



def calculateLightStop():
	for packet in packetsList:
		
		if packet[1] == "train-1":
			trainApproach = packet[2]
			break

	try:
		trainApproach = float(trainApproach)
	except ValueError:
		from datetime import datetime


		clean_string = trainApproach.replace("Z", "+00:00")

		dt_obj = datetime.fromisoformat(clean_string)

		unix_timestamp = dt_obj.timestamp()
		trainApproach = unix_timestamp
	currentTime = float(time.time())
	print(round(trainApproach - currentTime))
	return round(trainApproach - currentTime)

def getTrainGroup():
	TlightStates = fetchLightStates()
	for light in TlightStates:
		if TlightStates[light]['state'] == "green":
			switchLightState(light)
	selectedGroup = findGroups("train-1")	
	for key in selectedGroup:
		selectedGroup = selectedGroup[key] 
	
	return selectedGroup


def setTrainState(state: str):
	lightStates = fetchLightStates()

	for light in lightStates:
		if light == "train-1":
			print("overwriting train state...")
			
			lightStates[light]['state'] = state
	jsonStates = json.dumps(lightStates, indent=4)	
	with open("json/light_state.json", 'w') as file:
		file.write(jsonStates)		

def getTrainState():
	lightStates = fetchLightStates()
	if lightStates != None:
		return lightStates['train-1']['state']


def setLightState(state: str, id):
	lightStates = fetchLightStates()

	for light in lightStates:
		if light == str(id):
			print(f"overwriting {id} state...")
			
			lightStates[light]['state'] = state
	jsonStates = json.dumps(lightStates, indent=4)	
	with open("json/light_state.json", 'w') as file:
		file.write(jsonStates)		


