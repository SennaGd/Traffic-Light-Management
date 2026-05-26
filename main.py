from recieve_packets import * 
from json import JSONDecodeError
from doctest import debug

import uvicorn
import contextlib
import threading
import time
import subprocess 

from send_packet import *
from select_group import *
from calculate_amount import *
from toggle_light import * 
from train_check import *
from reset_states import onStart, resetLightStates

clear = lambda: subprocess.run("clear")

class APIServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        except KeyboardInterrupt:
            self.should_exit = True
            thread.join()

# responsible for parsing packetsList
class LoopHandler():
	def parseLights(self):	
		"""Loop for making sure the traffic lights turn on/off in order"""

		threads = [] 
		selectedGroup = []

		greenState = False	
		trainState = False		

		while True:

			gateClosing = False		
			try:
				packetsList = updatePacketsList()
			except json.JSONDecodeError:
				continue # run loop again

			# check for trainPacket
			fetchedTrainPacket = False
			trainTimeApproach = 10000000
			closing, closed = False, False
			trainSleeping = False
			currentTime = time.time()
			
			# fetched train packet
			for packet in packetsList:
				if packet[1] == "train-1":
					trainTimeApproach = packet[2]
					fetchedTrainPacket = True
					break

			timeBeforeTrain = float(trainTimeApproach)-currentTime
			
			# TRAIN
			# -  checks for time difference from current time
			# -  closing state T-10
			if timeBeforeTrain < 20 and fetchedTrainPacket:
				try:
					if closing and closed == False:
						switchOffLights() # switch lights off because closing
						setTrainState("closing")
				except json.JSONDecodeError:
					continue
				closing = True
			
			# -  fixed time sleep toggling the train group
			# -  closed state T-0
			if timeBeforeTrain < 10 and fetchedTrainPacket:
				closed = True
				selectedGroup = getTrainGroup()	
					
				# set light on green | gate: closed
				setTrainState("closed")
				deletePackets('train-1', 1, packetsList)
						
				for lightId in selectedGroup:
					setLightState('green', lightId)

				postToFrontEnd(url, gateClosing)

				print('sleeping')				
				time.sleep(20)
				print('done sleeping')

				for lightId in selectedGroup:
					setLightState('red', lightId)

				setTrainState("open") # open after 20 seconds	
				postToFrontEnd(url, gateClosing)

				continue # run loop again
				
			# update lightStates	
			# -  fetches lightStates | will exit loop iteration if decode error
			try:
				with open('json/light_state.json', 'r') as file:
					lightStates = json.load(file)
			except json.JSONDecodeError:
				continue
			
			trainState = lightStates['train-1']['state']


			# VEHICLES
			# -  only toggle whenever every light is red | packetsList cannot be []
			if greenState == False and len(packetsList) != 0 and trainState == "open" and trainSleeping == False:
				lightArray = fetchVehicleAmount(packetsList)

				currentPacket = packetsList[0]
				currentId = currentPacket[1]

				# skip current train packet | train is not coming yet
				if currentId == 'train-1':	
					try:
						currentPacket = packetsList[1]
					except IndexError:
						print('indexError')
						continue
					
				# finding groups for "id"	
				groupList = findGroups(currentId)
				selectedGroup, prevGroupIndex = sortGroup(lightArray, groupList, currentPacket)
				
				prevGroup = selectedGroup[len(selectedGroup)-1]
				
				 


				# dictionary used for calculating amount to delete 
				timeDict = getTotalTime(selectedGroup, packetsList)
				
				# make sure train-1 won't be toggled
				index = 0
				for id in selectedGroup:
					if id == "train-1":
						del(selectedGroup[index])	

					index += 1
				
				# fetch lightsStates | exit iteration if json decode error
				try:
					with open('json/light_state.json', 'r') as file:
						lightStates = json.load(file)
				except json.JSONDecodeError:
					continue

				# prevent lights from turning green whenever lights are still active
				for groupId in selectedGroup:
					for stateId in lightStates:
						if groupId != stateId and lightStates[stateId]['state'] == "green":
							continue
				
				# DELETING PACKETS
				# -  delete calculated amount of packets
				deletedTimeDict = False
				for key in timeDict:
					if key == "train-1":
						deletedTimeDict = True	

					if deletedTimeDict == False:
						deletePackets(key, timeDict[key][1], packetsList)
				
				print(selectedGroup, len(threads))

				# TOGGLING LIGHTS
				# start green light state
				for index in range(len(selectedGroup)):
					x = threading.Thread(target=switchLight, args=(selectedGroup[index], ))
					threads.append(x)
				
				for t in threads:
					t.start()

				postToFrontEnd(url, gateClosing)
				greenState = True

			# RUNNING VEHICLE LIGHTS
			# -  check if thread threads are still running | delete if not
			index = 0
			for thread in threads:
				if thread.is_alive() == False:
					del(threads[index])
					postToFrontEnd(url, gateClosing)
				index += 1
			

			print(len(threads))
			# checks if threads list is empty | if empty greenState is False 
			if len(threads) == 0:
				time.sleep(3)
				greenState = False

if __name__ == '__main__':
	for i in range(5):
		onStart()
	postToFrontEnd(url, gateClosing=False)
	print(time.time())
	config = uvicorn.Config("recieve_packets:app", host="0.0.0.0", port=8000) 
	server = APIServer(config=config)

	with server.run_in_thread():
		LoopHandler().parseLights() 
