from recieve_packets import * 
from json import JSONDecodeError
from doctest import debug

import uvicorn
import contextlib
import threading

from send_packet import *
from select_group import *
from calculate_amount import *
from toggle_light import * 
from train_check import *

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

		appendedId = False
		selectedGroup = []
		while True:
			gateClosing = False		
			trainApproach = False
			try:
				packetsList = updatePacketsList()
			except JSONDecodeError as e:
				print(e)
				packetsList = [] # make sure packetsList is empty on read error
			
			# check for trainPacket
			trainApproach = checkForTrain() 
			if trainApproach:
				timeBeforeTrain = calculateLightStop()	
				# turn off all lights | turn only T light (group) on
				if timeBeforeTrain < 6:
					selectedGroup= getTrainGroup(appendedId)
					gateClosing = True
				else:
					trainApproach = False
					
				if timeBeforeTrain < 0:
					selectedGroup= getTrainGroup(appendedId)
					gateClosing = False # gate should be closed
				else:
					trainApproach = False
			else:
				# if the time is not less than one minute keep normal loop going
				trainApproach = False
				
			# only toggle whenever every light is red | packetsList cannot be []
			if greenState == False and len(packetsList) != 0 and trainApproach == False:
				lightArray = fetchVehicleAmount(packetsList)

				currentPacket = packetsList[0]
				currentId = currentPacket[1]

				# finding groups for "id"	
				groupList = findGroups(currentId)
				selectedGroup, _ = sortGroup(lightArray, groupList, currentPacket)
				timeDict = getTotalTime(selectedGroup, packetsList)

				# start green light state
				for index in range(len(selectedGroup)):
					x = threading.Thread(target=switchLight, args=(selectedGroup[index], ))
					threads.append(x)
					x.start()	
				
				# delete calculated amount	of packets
				for key in timeDict:
					deletePackets(key, timeDict[key][1], packetsList)
				
				postToFrontEnd(url, gateClosing)
				greenState = True
				
			# if trainApproach is true enable the group
			elif trainApproach == True and timeBeforeTrain < 0:
				for index in range(len(selectedGroup)):
					print(index)
					x = threading.Thread(target=switchLight, args=(selectedGroup[index],))
					threads.append(x)
					x.start()	
				greenState = True
			try:
				timeBeforeTrain = calculateLightStop()	
				if timeBeforeTrain < -20:
					deletePackets("train-1", 1, packetsList)

			except UnboundLocalError:
				pass	

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
			print('h')

if __name__ == '__main__':

	config = uvicorn.Config("recieve_packets:app", host="0.0.0.0", port=8000, log_level="debug")

	server = APIServer(config=config)

	with server.run_in_thread():
		LoopHandler().parseLights() 
