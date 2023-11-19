from fastapi import FastAPI
from controller.connector import MqttHandler, process_data
from model.Score import onLoadEvent, calc_profit, calculate_distance
import queue, threading
import pandas as pd
import model.Load, model.Driver

app = FastAPI()
global TRUCKS = {} # List[dict] w/time
# id
# equiptype
# length
# time
global NOTIFS = {}
# """
# key : list

# element of the list is message :
# - load id,
# - Profit
# - Distance away
# - hour:minute 24hour format

# """

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/truck")
def list_trucks():
    # Return list of all truck IDs
    # Turns dict into list
    unique_trucks = list(TRUCKS.values())
    return unique_trucks


@app.get("/truck/{id}/notifications")
def get_notifications_for_truck(id: int):
    # Return a list of all the notifications the trucker has gotten
    return NOTIF.get(id)

def build_msg(load:Load, driver: Driver):
    return {
        'id': load.id,
        'profit': calc_profit(load, driver),
        'distance': calculate_distance(driver.location, load.origin),
        'time': f"{load.hour}:{load.minute}"
    }

def build_truck_profile(truck: Driver) -> dict:
    return{
        'id':truck.id,
        'equipType': truck.equipType,
        'tripLengthPref':truck.tripLengthPref,
        'time': f"{load.hour}:{load.minute}"
    }

if __name__ == '__main__':
    # Thread-Safe Queue
    message_queue = queue.Queue()

    # Set Up Handler
    handler = MqttHandler(message_queue)

    # Threads Setup
    listener_thread = threading.Thread(target=handler.listen)

    # Start Listener Thread
    listener_thread.start()


    # NOTIF = {}      # might cause issues where its declared
    # NOTIF_QUEUE = queue.Queue() # thread safe Priority queue is a built-in that is also thread safe
    # Global

    def periodically_process_data():
        import time
        while True:
            if not message_queue.empty():
                truck_df, load_df, eod = process_data(message_queue)
                # You can now use truck_data and load_data DataFrames
                # For example, print them, analyze, or save to CSV
                # print(truck_data, load_data)
                print("Truck Data")
                print(truck_data.head())
                print("Load Data")
                print(load_data.head())

                for i, new_load in load_df.iterrows(): #new_load is a row, # 'row' is a Series containing the row data # You can access specific columns using row['column_name']
                    for i, truck in truck_df.iterrows():

                        current_time = (
                            new_load["hour"],
                            new_load["minute"],
                            new_load["day_of_week"],
                            new_load["is_weekend"]
                            )

                        new_load = Load.buildInstanceFromSeries(new_load)
                        driver = Driver.buildInstanceFromSeries(truck)

                        # Notification
                        if onLoadEvent(new_load, current_time, driver): # on load event returns if you should be notified (None otherwise)
                            msg = build_msg(new_load, driver)

                            if NOTIF.get(driver.id) is None:
                                NOTIF[driver.id] = [msg]
                            else:
                                NOTIF[driver.id].append(msg)

                        # Updating Truck list
                        TRUCKS[driver.id] = build_truck_profile(driver)


            time.sleep(5)  # Process every 5 seconds

    # Start periodic processing in a separate thread
    processor_thread = threading.Thread(target=periodically_process_data)
    processor_thread.start()
