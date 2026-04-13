import json

with open("light_order.json", "r") as file:
    valid_paths = json.load(file)



with open("trafficlightlist.json", "r") as file:
    opened_json = json.load(file)
   

class Node():
    def __init__(self, lightId):
        self.lightId = lightId
        self.next = None
        
 
head = Node(2.1) 
node2 = Node(4.1)
node3 = Node(6.1)

head.next = node2
node2.next = node3

temp = head   

def Get_light_state(light_id):
    return opened_json[str(light_id)]['state']


def Switch_light_state(light_id):
    # switching light states
    if (Get_light_state(str(light_id)) == "red"):
        opened_json[str(light_id)]['state'] = "green"
        
    elif (Get_light_state(str(light_id)) == "green"):
        opened_json[str(light_id)]['state'] = "red"
    
    
    print(opened_json)
    
    
    with open("new.json", "w") as f:
        json.dump(opened_json, f)


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

def Toggle_light():
    for light_categories in opened_json:
        print(light_categories)
    
    
def Toggle_group():
    ...




def Check_toggleable():
    #? checks if the path can be set to green
    
    selected_light = 4.1 # check all possible paths for 8.1
    
    #? all possible paths that 'selected_light' can take
    light_paths = valid_paths[str(selected_light)]
    print(light_paths)
    paths = []
    i = 0
    for groups in light_paths:
        for path in groups[str(i)]:
            print(path)
            paths.append(path)
            
        i+=1
        
        
    print(paths)
        
        
        
    for light in opened_json:
        if (light not in paths):
            if (opened_json[light]['state'] == "green"):
                print(light, ': green')
                return False
            else:
                print(light, ': red') 
                
            
    
        
Parse_packet()


# Check_toggleable()