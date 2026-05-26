import requests
from structs.packets import *
from structs.post_state import *
from json_variables import *
  
ip = '172.16.48.244'
port = '5001'

url = "http://" + ip + ':' + port + '/receive'

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

		print('posting')
		x = requests.post(url, json=payload)
		print(x.status_code)
	except:
		print('postFailed')
		pass


