from fastapi import FastAPI
from controller.connector import MqttHandler, Processor
from model.Score import onLoadEvent, calc_profit, calculate_distance
import queue, threading
import pandas as pd
from model.Load import Load
from model.Driver import Driver
from typing import Tuple
import time

app = FastAPI()
global TRUCKS
TRUCKS = {} # List[dict] w/time
# id
# equiptype
# length
# time
global NOTIFS
NOTIFS = {}
# """
# key : list

# element of the list is message :
# - load id,
# - Profit
# - Distance away
# - hour:minute 24hour format

# """
global LOADS
load_cols = ['seq', 'type', 'loadId', 'originLatitude', 'originLongitude', 'destinationLatitude', 'destinationLongitude', 'equipmentType', 'price', 'mileage',
            "hour","minute","day_of_week","is_weekend"]
LOADS = pd.DataFrame(columns = load_cols)


def on_startup():
    # Thread-Safe Queue
    message_queue = queue.Queue()

    # Set Up Handler
    handler = MqttHandler(message_queue)

    processor = Processor()

    # Threads Setup
    listener_thread = threading.Thread(target=handler.listen)

    # Start Listener Thread
    listener_thread.start()

    # NOTIF = {}      # might cause issues where its declared
    # NOTIF_QUEUE = queue.Queue() # thread safe Priority queue is a built-in that is also thread safe
    # Global

    def periodically_process_data():
        global TRUCKS
        global NOTIFS
        global LOADS
        while True:
            if not message_queue.empty():
                truck_df, load_df, eod = processor.process_data(message_queue)
                # You can now use truck_data and load_data DataFrames
                # For example, print them, analyze, or save to CSV

                if eod: #Reset everything
                    TRUCKS = {}
                    NOTIFS = {}
                    LOADS = pd.DataFrame(columns = load_cols)
                    continue

                for j, new_load in load_df.iterrows(): #new_load is a row, # 'row' is a Series containing the row data # You can access specific columns using row['column_name']
                    for i, truck in truck_df.iterrows():

                        current_time = (
                            new_load["hour"],
                            new_load["minute"],
                            new_load["day_of_week"],
                            new_load["is_weekend"]
                            )

                        load = Load.buildInstanceFromSeries(new_load)
                        driver = Driver.buildInstanceFromSeries(truck)

                        # Notification
                        check_and_notify(load, driver, current_time)

                        # If new driver => calc all loads => add to TRUCKS making it no longer a new driver <= do so in the next line
                        if not TRUCKS.get(driver.id):
                            consider_old_loads(truck, driver)

                        # Updating Truck list
                        TRUCKS[driver.id] = build_truck_profile(driver)

            time.sleep(0.5)  # Process every 5 seconds

    # Start periodic processing in a separate thread
    processor_thread = threading.Thread(target=periodically_process_data)
    processor_thread.start()

# Register the on_startup function to be called when the application starts
app.add_event_handler("startup", on_startup)


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
    return NOTIFS.get(id)


def build_msg(load:Load, driver: Driver, time: Tuple[int, int, int, int]):
    return {
        'id': load.id,
        'profit': calc_profit(load, driver),
        'distance': calculate_distance(driver.location, load.origin),
        'time': f"{time[0]}:{time[1]}"
    }


def build_truck_profile(truck: Driver) -> dict:
    return {
        'id':truck.id,
        'equipType': truck.equip_type,
        'tripLengthPref':truck.trip_length_preference,
        'time': f"{truck.hour}:{truck.minute}"
    }


def consider_old_loads(truck: pd.Series, driver: Driver):
    for k, old_load in LOADS.iterrows():
        current_time = (
            truck["hour"],
            truck["minute"],
            truck["day_of_week"],
            truck["is_weekend"]
        )
        load = Load.buildInstanceFromSeries(old_load)

        check_and_notify(load, driver, current_time)
    

def check_and_notify(load: Load, driver: Driver, current_time:Tuple[int, int, int, int]) -> None:
    '''
    Checks if you need to send a notif to a driver for a particular load, and if so, adds
    it to the notif global var
    '''
    if onLoadEvent(load, current_time, driver):
        msg = build_msg(load, driver, current_time)

        if NOTIFS.get(driver.id) is None:
            NOTIFS[driver.id] = [msg]
        else:
            NOTIFS[driver.id].append(msg)
    