# this file is for making sure the train closes on T-10 and closed on T0

import time
from json_variables import *

trainArrive = time.time()+20

trainState = 'open'


# if trainPacket; calculate time
# if time of arrival bigger than current time + 10
# ^ -> state is open
# if time of arrival smaller than time + 10
# ^ -> state is closing | disable all states
# if time of arrival smaller than time
# ^ -> state = closed | trainGroup on

while True:
	if trainArrive > time.time() + 10:
		trainState = "open"
	if trainArrive < time.time() + 10:
		trainState = "closing"

	if trainArrive < time.time():
		trainState = "closed"

	print(trainState)
