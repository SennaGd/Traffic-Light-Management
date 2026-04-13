import json
# writes packet into other json file
# clears packet file


def Insert_in_list():
    with open("json/recieved_packet.json","r") as f:
        packet_file = json.load(f)
        
    with open("json/packet_list.json", "r") as file:
        packet_list = json.load(file)
           
    # print(packet_file)
    for packet in packet_file["messages"]:
        print(packet['message']['id'])
        print(packet['type'])
        new_packet = packet['type'], packet['message']['id']
        packet_list.append(new_packet)
        
        
    with open("json/packet_list.json", "w") as f:
        json.dump(packet_list, f)
    
    with open("json/recieved_packet.json","w") as f:
       json.dump( {}, f)
    
Insert_in_list()