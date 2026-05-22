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

def getTrainGroup(appendedId: bool):
	TlightStates = fetchLightStates()
	for light in TlightStates:
		if TlightStates[light]['state'] == "green":
			switchLightState(light)
	selectedGroup = findGroups("train-1")	
	for key in selectedGroup:
		selectedGroup = selectedGroup[key] 
	
	# append only once
	if appendedId == False:
		selectedGroup.append("train-1")
		
		
	return selectedGroup

