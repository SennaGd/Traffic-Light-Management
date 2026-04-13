import json

with open("light_order.json", "r") as file:
    valid_paths = json.load(file)



with open("trafficlightlist.json", "r") as file:
    opened_json = json.load(file)
   

class Node():
    def __init__(self, lightId = None):
        self.lightId = lightId
        self.next = None
        
 
head = Node() 
node1 = Node(2.1)
end_node = Node()

head.next = node1
node1.next = end_node


def Get_light_state(light_id):
    try:
        return opened_json[str(light_id)]['state']
    except KeyError as E: 
        return 
    
    


def Switch_light_state(light_id):
    switched_state = False
    # switching light states

    if (Get_light_state(str(light_id)) == "red" and not switched_state):
        opened_json[str(light_id)]['state'] = "green"
        print("Switched from red -> green")
        switched_state = True
    
    elif (Get_light_state(str(light_id)) == "green" and not switched_state):
        opened_json[str(light_id)]['state'] = "red"
        print("Switched from green -> red")
        
        switched_state = True
        
    
    with open("trafficlightlist.json", "w") as f:
        json.dump(opened_json, f)

temp = head   
while temp.next is not None:
    # print(temp.lightId, end=" \n")
    
    state = Get_light_state(temp.lightId)
    Switch_light_state(temp.lightId)
    
    temp = temp.next

   
def Parse_packet():
    with open("testpacket.json", "r") as file:
        packet = json.load(file)
        print(packet["messages"][0]['type'])
        print(packet["messages"][0]["message"]["id"])

    
    
def Toggle_group():
    ...



