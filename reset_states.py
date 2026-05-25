# file will reset ALL packets upon launching the server
from json_variables import *

def resetLightStates():
	with open('json/light_state.json', 'r') as file:
		lightStates = json.load(file)
	
	for light in lightStates:
		if light != "train-1":
			if lightStates[light]['state'] == "green":
				lightStates[light]['state'] = "red"

			if lightStates[light]['time-toggled'] != 0:
				lightStates[light]['time-toggled'] = 0
		else:
			lightStates[light]['state'] = "open"
	parsedStates = json.dumps(lightStates, indent=4)	
	with open('json/light_state.json', 'w') as file:
		file.write(parsedStates)


def onStart():
	resetLightStates() # resets states to red
	overWritePacketsList([]) # removes all packets
