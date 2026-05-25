# json variables that are used in multiple files

import json
import time
from datetime import datetime, timezone
from structs.packets import Packet



with open("json/light_order.json", "r") as file:
	lightGroups = json.load(file)

with open("json/light_state.json", 'r') as file:
	try:
		lightStates = json.load(file)
	
	except json.JSONDecodeError as e:
		print("Line 18:", e)


with open('json/packets.json', 'r') as file:
	packetsList = json.load(file)


def updatePacketsList():
	with open('json/packets.json', 'r') as file:
		packetsList = json.load(file)

	return packetsList

def fetchLightStates():
	with open('json/light_state.json', 'r') as file:
		light_States = json.load(file)
	return light_States 

def overWritePacketsList(newList):
	strList = json.dumps(newList, indent=4) 
	with open("json/packets.json", "w") as file:
		file.write(strList)

# checks time format
def checkTimeFormat(packetTime):
    if isinstance(packetTime, (int, float)):
        return "Time"
    
    if isinstance(packetTime, str):
        if "T" in packetTime and "-" in packetTime:
            return "ISO"
            
    return "unknown"

def insertIntoPacketsList(packet: Packet):
	with open("json/packets.json", "r") as file:
		# packetList = json.load(file)
		packetList = json.load(file)
	timeFormat = checkTimeFormat(packet.message.expectedArrival)
	if timeFormat == "ISO":
		iso_string = str(packet.message.expectedArrival)
		
		if iso_string.endswith('Z'):
			iso_string = iso_string.replace('Z', '+00:00')
		
		dateTime = datetime.fromisoformat(iso_string)
		if dateTime.tzinfo is None:
			dateTime = dateTime.replace(tzinfo=timezone.utc)
		arrivalTime = str(dateTime.timestamp())
		arrivalTime = arrivalTime.split('.')[0]
	else:
		arrivalTime = packet.message.expectedArrival

	packetList.append([packet.type, packet.message.id, arrivalTime, int(time.time())])
   
	with open("json/packets.json", "w") as file:
		json.dump(packetList, file, indent=4)

