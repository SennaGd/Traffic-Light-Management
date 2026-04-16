# package imports
import json
import time

# file imports
from PriorityList import create_priority_list
from classes import Node


with open("json/light_order.json", "r") as file:
    valid_paths = json.load(file)

with open("json/light_state.json", "r") as file:
    opened_json = json.load(file)


# returns the state of light_id
def Get_light_state(light_id) -> str | None:
    try:
        return opened_json[str(light_id)]['state']
    except KeyError as E:
        return


# switches the light on/off
def Switch_light_state(light_id) -> None:
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


def Check_light_group(light_id=None, next_light_id=None) -> dict | None:
    try:
        groups = valid_paths[light_id]
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

            group_array.append(values)  # append values to groups array

        # sort the array
        i = 0
        for group in group_array:
            group_array[i] = sorted(group)

            i += 1
        return group_array  # return list
    else:
        return None  # if groups was not valid


# insert nodes
def Node_insert(head, x):
    newNode = Node(x)

    if (head is None):
        return newNode

    temp = head
    while temp.next is not None:
        temp = temp.next

    temp.next = newNode

    return head

# fetches valid paths | groups


def Fetch_groups(light_id: str) -> dict | None:
    try:
        return valid_paths[str(light_id)]
    except KeyError:
        print("valid path is nonexistent")
        return


def Parse_groups(groups_dict: dict) -> list | None:
    if (not groups_dict):
        return None

    group: list = []
    for key in groups_dict:
        group += [groups_dict[key]]

    return group


# checks if 
def Check_compatible_group(group_list: list, light_id) -> list:
    node = head
    while node is not None:
        if (str(node.light_id) == light_id):
            current_node = node
            break
        node = node.next

    node = current_node  # current node

    # checking if next nodes are equal to current node's group's
    while node is not None:
        # prevent nonetype
        if (group_list is None):
            break
        # parse all groups inside
        # fetch selected group based upon recent vehicles
        for group in group_list:
            for value in group:
                if (node.light_id == value):
                    return group

        node = node.next


# responsible for adding the light_id if it is not inside the selected_group
def parse_selected_group(light_id, selected_group: list | None) -> list:
    if (selected_group is None):
        # toggle only 1 light
        return [light_id]
    else:
        for value in selected_group:
            if (light_id == value):
                inside_group = True
            else:
                inside_group = False

        if (not inside_group):
            selected_group.append(light_id)

        return selected_group


# traverses the nodes
def Traverse_nodes(head: Node) -> None:
    node = head
    index = 0
    while node is not None:
        print("Node index:", index, "Node Id:", node.light_id)
        light_id = str(node.light_id)

        groups = Fetch_groups(light_id)
        group_list = Parse_groups(groups)

        # parse next nodes seperate | check if there's reoccuring node values in group
        selected_group = Check_compatible_group(group_list, light_id)
        selected_group = parse_selected_group(node.light_id, selected_group)

        # toggling the light group | running simultaniously
        print("group",selected_group)
        index += 1
        node = node.next  # next node


head = Node()
priorityList = create_priority_list("json/packets.json", head)
for light in priorityList:
    Node_insert(head, light)


Traverse_nodes(head)
# Traverse list of packets
