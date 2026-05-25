from json_variables import packetsList, lightStates, updatePacketsList, overWritePacketsList

selectedGroup = ['2.1', '8.1']
packetsList = updatePacketsList()
def getTotalTime(selectedGroup: list, packetsList: list) -> dict[str, list]:
	"""Calculates the total time for all packets on {id}"""

	diffList = {}
	# creating dictionary with groups & time differences
	for group in selectedGroup:
		diffList[group] = []
		prevTime = None
		for _, id, _, time in packetsList:
			if group == id :
				if prevTime is None:
					prevTime = time

				timeDiff = time - prevTime
				if timeDiff != 0.0:
					diffList[group].append(timeDiff)

				prevTime = time
	totalTime = {} 
	for key in diffList:
		totalTime[key] = [0,1]
		for diffs in diffList[key]:
			if totalTime[key][0] <= lightStates[key]['enabled-time']:
				totalTime[key][0] += (diffs + 1)
				totalTime[key][1] += 1 # Append packet

			if totalTime[key][0] == 0:
				totalTime[key][0] = 1

	return totalTime
timeDict = getTotalTime(selectedGroup, packetsList)


def deletePackets(id: str, amount, packetsList):
	"""Removes x amount of packets from packetslist"""
	print('deleting', id)
	deleted = 0
	index = 0
	for _, packetId, _, _ in packetsList:
		if packetId == id:
			del(packetsList[index])
			deleted += 1

		if deleted == amount:
			overWritePacketsList(packetsList)	
			return True
		index += 1



