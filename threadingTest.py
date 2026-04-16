import json
import threading
import time

with open("json/light_state.json", "r") as file:
    opened_json = json.load(file)


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


def Switch_light(light_id):
    state = opened_json[str(light_id)]['state']

    if (state == "red"):
        Switch_light_state(light_id)  # toggle on

        # time variables
        time_toggled = opened_json[str(light_id)]['time-toggled']
        time_amount = opened_json[str(light_id)]["enabled-time"]

        # countdown | hold green for X seconds
        time_left = int(time.time())
        while (int(time.time()) != time_toggled+time_amount):
            # if runs every tick | inside if runs ever second
            if (time_left == time_toggled+time_amount - int(time.time())):
                time_left = time_toggled+time_amount - int(time.time())
            print(opened_json[str(light_id)]['state'])
            # print(time_toggled+time_amount - int(time.time()))

        Switch_light_state(light_id)  # toggle off


group = [3.1, 4.1, 2.1]

threads = list()
# get len(group) threads running.
for index in range(len(group)):
    x = threading.Thread(target=Switch_light, args=(group[index], ))
    threads.append(x)
    x.start()
