import json

# return ordered priority list
def create_priority_list(filename, head)->list:
    with open(filename, 'r') as f:
        file = json.load(f)
        
    vehicles_on_light = []  
    for packet in file:
        if (packet[0] == "vehicleWaiting" or packet[0] == "pedestrianWaiting"):
            vehicles_on_light.append(packet[1])
        
    priorityList = {i: vehicles_on_light.count(i) for i in vehicles_on_light}
    
    head.next = None # reset the list
    
    # parse from dict -> list
    tempList = []
    for id in priorityList:
        priority = priorityList[id]
        # append new list reverse order (priority, light_id)
        tempList.append([priority,id])
        
    priorityList = sorted(tempList, reverse=True) # highest priority first
    
    # revert reversed order (light_id, priority)
    tempList = []
    for light in priorityList:
        tempList.append([light[1],light[0]])
        
    priorityList = tempList
    
    
    print(priorityList)
    
    orderList = []
    for light in priorityList:
        orderList.append(light[0])    

    return orderList
    

# create_priority_list("json/packets.json", head)

