# Responsible for selecting the right group based on packet amount 
# Will create variable called: selectedGroup

from json_variables import * 


def fetchVehicleAmount(packetsList):
	lights = {} 
	for light in lightStates:
		lights[light] = 0 
	
	for _, packet, _, _ in packetsList: 
		for light in lights:
			if light == packet:
				lights[light] += 1

	return lights

def findGroups(currentId: str) -> list:
	groups = lightGroups[currentId]
	return groups


# finds group based on priority
def sortGroup(lightArray: dict, groupList: list, currentPacket):	
	# Prioritising groups
	print("groupList", groupList)
	groupCount = {}
	selectedGroup = 0 # this is an index
	for group in groupList:
		groupCount[group] = 0
		for id in groupList[group]:
			if lightArray[str(id)] > 0:
				print(lightArray[str(id)])
				groupCount[group] += lightArray[str(id)]

	highest = 0
	for x in groupCount:
		if groupCount[x] > highest:
			highest = groupCount[x]
			selectedGroup = x

	# adding the currentId to group | making sure the id isn't duplicated
	appendedId = False # check if the id is appended
	for group in groupList[str(selectedGroup)]:
		if currentPacket[1] == group:
			appendedId = True

	if appendedId == False:
		groupList[str(selectedGroup)].append(currentPacket[1])

	FetchedSelectedGroup = groupList[str(selectedGroup)]

	# parsing group ids to str
	index = 0
	for id in FetchedSelectedGroup:
		if type(id) is int | float:
			FetchedSelectedGroup[index] = str(id)	
		index += 1

	
	# check if all lights have to be toggled or less
	finalGroup = []
	for group in FetchedSelectedGroup:
		for _, id, _, _ in packetsList:
			if str(group) == id and id not in finalGroup:
				finalGroup.append(str(id))

	return FetchedSelectedGroup, highest 

