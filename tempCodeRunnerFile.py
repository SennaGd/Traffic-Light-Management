    Switch_light_state(light_id) # toggle on
            
            # time variables
            time_toggled = opened_json[str(light_id)]['time-toggled']
            time_amount = opened_json[str(light_id)]["enabled-time"]
            
            # countdown | hold green for X seconds
            while(int(time.time()) != time_toggled+time_amount):
                time_left = time_toggled+time_amount - int(time.time())
                
                
                print("time left: ",time_left)
                
            Switch_light_state(light_id) # toggle off