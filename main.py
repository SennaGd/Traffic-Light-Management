import json
import time

with open("json/light_order.json", "r") as file:
    valid_paths = json.load(file)
    
with open("json/light_state.json", "r") as file:
    opened_json = json.load(file)
   
class Node():
    def __init__(self, light_id = None):
        self.light_id = light_id
        self.next = None   
        
# returns the state of light_id
def Get_light_state(light_id)->str | None:
    try:
        return opened_json[str(light_id)]['state']
    except KeyError as E: 
        return 
 
    
# switches the light on/off
def Switch_light_state(light_id)->None:
    switched_state = False
    # switching light states

    if (Get_light_state(str(light_id)) == "red" and not switched_state):
        opened_json[str(light_id)]['state'] = "green"
        opened_json[str(light_id)]['time-toggled'] = int(time.time())
        switched_state = True
    
    elif (Get_light_state(str(light_id)) == "green" and not switched_state):
        opened_json[str(light_id)]['state'] = "red"
        opened_json[str(light_id)]['time-toggled'] = 0
        switched_state = True
        
    
    with open("json/light_state.json", "w") as f:
        json.dump(opened_json, f)

# returns unsorted paths
def Check_light_group(light_id = None, next_light_id = None)->dict | None:
    try:
        groups = valid_paths[str(light_id)]        
        return groups
         
    except KeyError:
        print("non existent groups")


# returns sorted paths
def Order_light_group(groups: dict, light_id) -> list | None:
    if (groups is not None):
        
        # get unsorted groups | parse: dict -> list 
        group_array = []
        for group in groups: 
            values = [light_id]
            
            for value in groups[group]:
                values.append(value)
            
            group_array.append(values) #append values to groups array
            
        # sort the array    
        i = 0 
        for group in group_array:
            group_array[i] = sorted(group)
            
            i+=1
        return group_array # return list
    else:
        return None # if groups was not valid



     
       
def Node_insert(head, x):
    newNode = Node(x)
    
    if (head is None):
        return newNode
    
    temp = head
    while temp.next is not None:
        temp = temp.next
    
    temp.next = newNode
    
    return head   
  
  
# Toggle light -> set time -> wait till time == cur-time
# next node (repeat) ^ 
def Parse_list(node: Node):
    while node is not None:
        state = Get_light_state(str(node.light_id))
        light_id = node.light_id
        
        # print (id : red or green)
        if(str(light_id) != 'None'):
            print(f"{light_id}:{state}")

        # fetched next node light_id
        if (node.next is not None):
            next_light_id = node.next.light_id
        else:
            next_light_id = None
            
        # validating valid routes
        groups = Check_light_group(light_id, next_light_id)
        sorted_groups = Order_light_group(groups, light_id)
        
        # checking if valid routes are same as next id routes
        next_groups = Check_light_group(next_light_id)
        sorted_next_groups = Order_light_group(next_groups, next_light_id)    
        
        if (sorted_groups and sorted_next_groups):
            for group in sorted_groups:
                for nextgroup in sorted_next_groups:
                    print(group == nextgroup)
                    print(group, nextgroup)
                    
    
        # toggling lights | groups
        if(state == "red"):
            Switch_light_state(light_id) # toggle on
            
            # time variables
            time_toggled = opened_json[str(light_id)]['time-toggled']
            time_amount = opened_json[str(light_id)]["enabled-time"]
            
            # countdown | hold green for X seconds
            time_left = int(time.time())
            while(int(time.time()) != time_toggled+time_amount):
                # if runs every tick | inside if runs ever second
                if (time_left == time_toggled+time_amount - int(time.time())):
                    time_left = time_toggled+time_amount - int(time.time())
                    
                    print(time_toggled+time_amount - int(time.time()))

                    
                    
                    
                
            Switch_light_state(light_id) # toggle off

        
        node = node.next # next node
        

head = Node()
Node_insert(head, 3.1)
Node_insert(head, 2.1)
Node_insert(head, 3.1)


Parse_list(head)


# Traverse list of packets
