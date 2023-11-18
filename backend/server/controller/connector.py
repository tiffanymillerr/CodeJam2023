import sys
import os
sys.path.append(os.path.abspath("../model"))

import model.MqttHandler as mq
import threading
import queue
import pandas as pd
from typing import Tuple


# Define a function to process messages from the queue and update DataFrames
def process_data(message_queue: queue.Queue, 
                 truck_df: pd.DataFrame, 
                 load_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:

    while not message_queue.empty():
        json_data = message_queue.get()
        temp_df = pd.DataFrame.from_dict(json_data, orient='index').T
        tp = temp_df['type'].item().lower()

        if tp == 'start':
            # Reset DataFrames for new day
            truck_df = pd.DataFrame(columns=['seq', 'type', 'timestamp', 'truckId', 'positionLatitude', 'positionLongitude', 'equipType', 'nextTripLengthPreference'])
            load_df = pd.DataFrame(columns=['seq', 'type', 'timestamp', 'loadId', 'originLatitude', 'originLongitude', 'destinationLatitude', 'destinationLongitude', 'equipmentType', 'price', 'mileage'])
            print("Start of new day")
        elif tp == 'truck':
            print("Got truck")
            truck_df = pd.concat([truck_df, temp_df], ignore_index=True)
        elif tp == 'load':
            print("Got load")
            load_df = pd.concat([load_df, temp_df], ignore_index=True)
        elif tp == 'end':
            print("End of day")

    # Return DataFrames in case they need to be used immediately after calling
    return truck_df, load_df

# Define global DataFrames
truck_df = pd.DataFrame()
load_df = pd.DataFrame()

# Thread-Safe Queue
message_queue = queue.Queue()

# Set Up Handler
handler = mq.MqttHandler(message_queue)

# Threads Setup
listener_thread = threading.Thread(target=handler.listen)

# Start Listener Thread
listener_thread.start()

if __name__ == '__main__':
    # Example usage of process_data function
    def periodically_process_data():
        import time
        while True:
            if not message_queue.empty():
                truck_data, load_data = process_data(message_queue)
                # You can now use truck_data and load_data DataFrames
                # For example, print them, analyze, or save to CSV
                # print(truck_data, load_data)
                print("Truck Data")
                print(truck_data.head())
                print("Load Data")
                print(load_data.head())
            time.sleep(5)  # Process every 5 seconds

    # Start periodic processing in a separate thread
    processor_thread = threading.Thread(target=periodically_process_data)
    processor_thread.start()