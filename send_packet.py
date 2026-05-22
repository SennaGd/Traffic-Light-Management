import requests
from structs.packets import *
from structs.post_state import *
from json_variables import *

ip = '172.16.48'
subIp = '58'
port = '5501'

url = "http://" + ip + '.' + subIp + ':' + port + '/post'

def postToFrontEnd(url: str, gateClosing: bool):
	try:
		lightStates = fetchLightStates()

		payload = {
				"messages": []
		}
		
		
		for light in lightStates:
			if light != "train-1":
				payload["messages"].append(
						{"type":"trafficLightState",
						"message": {"id": str(light), "state":lightStates[light]['state']}})
				
			if light == "train-1" and gateClosing == True:
				payload["messages"].append(
					{"type":"crossingGate",
					"message": {"id": str(light), "state":"closing"}})

			if light == "train-1" and gateClosing == False:
				payload["messages"].append(
				{"type":"crossingGate",
				"message": {"id": str(light), "state":"closed"}})
				# remove packet and 	


		x = requests.post(url, json=payload)
		print('send to frontend!', x.status_code )
	except:
		pass


