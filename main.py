from recieve_packets import * 
from json import JSONDecodeError
from doctest import debug

import uvicorn
import contextlib
import threading
import time

from send_packet import *
from select_group import *
from calculate_amount import *
from toggle_light import * 
from train_check import *
from reset_states import onStart, resetLightStates

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

		threads = list()	
		greenState = False	
		trainState = False		
		selectedGroup = []

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

			# checks for time difference from current time
			# closing state T-10
			if timeBeforeTrain < 20 and fetchedTrainPacket:
				try:
					if closing and closed == False:
						switchOffLights() # switch lights off because closing
						setTrainState("closing")
				except json.JSONDecodeError:
					continue
				closing = True
			
			# fixed time sleep toggling the train group
			# closed state T-0
			if timeBeforeTrain < 10 and fetchedTrainPacket:
				closed = True
				selectedGroup = getTrainGroup()	
					
				# set light on green
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

			# make sure only one switch
						
			# try to fetch states
			try:
				with open('json/light_state.json', 'r') as file:
					lightStates = json.load(file)
			except json.JSONDecodeError:
				continue

			if lightStates != None:
				trainState = lightStates['train-1']['state']


			# only toggle whenever every light is red | packetsList cannot be []
			if greenState == False and len(packetsList) != 0 and trainState == "open" and trainSleeping == False:
				lightArray = fetchVehicleAmount(packetsList)

				currentPacket = packetsList[0]
				currentId = currentPacket[1]
				if currentId == 'train-1':	
					try:
						currentPacket = packetsList[1]
					except IndexError:
						print('indexError')
						continue
					
				# finding groups for "id"	
				groupList = findGroups(currentId)
				selectedGroup, _ = sortGroup(lightArray, groupList, currentPacket)

				timeDict = getTotalTime(selectedGroup, packetsList)
				
				index = 0
				for id in selectedGroup:
					if id == "train-1":
						del(selectedGroup[index])	

					index += 1

				# start green light state
				for index in range(len(selectedGroup)):
					x = threading.Thread(target=switchLight, args=(selectedGroup[index], ))
					threads.append(x)
					x.start()	
				
				# delete calculated amount	of packets
				deletedTimeDict = False
				for key in timeDict:
					if key == "train-1":
						deletedTimeDict = True	

					if deletedTimeDict == False:
						deletePackets(key, timeDict[key][1], packetsList)

				# TODO: REMOVE COMMENTED POST	
				postToFrontEnd(url, gateClosing)
				greenState = True


		    # when the gate is closing: pause all gates for minimum of 10 seconds

			# check if thread threads are still running | delete if not
			index = 0
			for thread in threads:
				if thread.is_alive() == False:
					del(threads[index])
					postToFrontEnd(url, gateClosing)
				index += 1
			# checks if threads list is empty | if empty greenState is False 
			if len(threads) == 0:
				greenState = False

if __name__ == '__main__':
	onStart()
	print(time.time())
	config = uvicorn.Config("recieve_packets:app", host="0.0.0.0", port=8000, log_level="debug")

	server = APIServer(config=config)

	with server.run_in_thread():
		LoopHandler().parseLights() 
