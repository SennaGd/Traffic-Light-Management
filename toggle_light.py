from json_variables import *

import time

lightStates = fetchLightStates()

def getLightState(lightId) -> str | None:
    try:
        return lightStates[str(lightId)]['state']
    except KeyError:
        return


# switches the light on/off
def switchLightState(lightId) -> None:
    switched_state = False
    # switching light states

    if (getLightState(str(lightId)) == "red" and not switched_state):
        lightStates[str(lightId)]['state'] = "green"
        lightStates[str(lightId)]['time-toggled'] = int(time.time())
        switched_state = True

    elif (getLightState(str(lightId)) == "green" and not switched_state):
        lightStates[str(lightId)]['state'] = "red"
        lightStates[str(lightId)]['time-toggled'] = 0
        switched_state = True
    with open("json/light_state.json", "w") as f:
        json.dump(lightStates, f)	


def switchLight(lightId):
	state = lightStates[str(lightId)]['state']

	if (state == "red"):
		switchLightState(lightId)  # toggle on
		print(lightId, lightStates[str(lightId)]['state'])

		# time variables
		timeToggled = lightStates[str(lightId)]['time-toggled']
		timeAmount = lightStates[str(lightId)]["enabled-time"]

		# countdown | hold green for X seconds
		timeLeft = int(time.time())
		while (int(time.time()) != timeToggled+timeAmount):
			# if runs every tick | inside if runs ever second
			if (timeLeft == timeToggled+timeAmount - int(time.time())):
				timeLeft = timeToggled+timeAmount - int(time.time())
		
		switchLightState(lightId)  # toggle off
		print(lightId, lightStates[str(lightId)]['state'])
