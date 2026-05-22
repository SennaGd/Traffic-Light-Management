# json variables that are used in multiple files

import json
import time

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

def insertIntoPacketsList(packet: Packet):
	with open("json/packets.json", "r") as file:
		# packetList = json.load(file)
		packetList = json.load(file)
	
	packetList.append([packet.type, packet.message.id, packet.message.expectedArrival, int(time.time())])
   
	with open("json/packets.json", "w") as file:
		json.dump(packetList, file, indent=4)

