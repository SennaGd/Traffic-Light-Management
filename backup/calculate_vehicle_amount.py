# responsible for calculating how many packets to delete in packets.json
from json_variables import packetsList, lightStates, updatePacketsList, overWritePacketsList

selectedGroup = ['2.1', '8.1']

def createMedianDict(selectedGroup: list, packetsList: list) -> dict[str, float]:
	"""creates median dictionary containing all medians for each group"""
	diffList = {}

	# creating dictionary with groups & time differences
	for group in selectedGroup:
		diffList[group] = []
		index = 0
		prevTime = None
		for _, id, _, time in packetsList:
			if group == id and index != 0:
				if prevTime is None:
					prevTime = time

				timeDiff = time - prevTime
				if timeDiff != 0.0:
					diffList[group].append(timeDiff)

				prevTime = time

			index += 1

    # creating median dictionary
	medianDict = {}
	for key in diffList:
		
		total = 0.0
		for difference in diffList[key]:
			total += difference

		diffListKeyLength = len(diffList[key])
		if diffListKeyLength > 0:
			median = total/len(diffList[key])
		else:
			median = 0.0 # 0.0 will be just 1 packet

		medianDict[key] = median

	return medianDict


def calculatePacketAmount(medianDict: dict, lightStates: list) -> dict[str, int]:
	packetAmount = {} 

	for key in medianDict:
		for light in lightStates:
			if light == key:
				if medianDict[key] != 0:
					amount = lightStates[light]['enabled-time']/medianDict[key] 
				else:
					amount = 1

				if amount < 1:
					amount = 1
				else:
					amount = round(amount)

				packetAmount[key] = amount

	return packetAmount
medianDict = createMedianDict(selectedGroup, packetsList) 
packetAmount = calculatePacketAmount(medianDict, lightStates)
print(packetAmount)
