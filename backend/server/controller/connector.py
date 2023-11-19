import sys
import os
# sys.path.append(os.path.abspath("../model"))
# import model.Score as Score
import threading
import queue
import pandas as pd
from typing import Tuple

import paho.mqtt.client as mqtt
import json

class MqttHandler:
    # MQTT Settings
    MQTT_BROKER = "fortuitous-welder.cloudmqtt.com"
    MQTT_PORT = 1883
    MQTT_TOPIC = "CodeJam"
    MQTT_USERNAME = "CodeJamUser"
    MQTT_PASSWORD = "123CodeJam"
    CLIENT_ID = "GDSC01"  # Replace with your team name

    def __init__(self, queue):
        self.queue = queue
        self.cur_day = 0
        self.daytime = True #on first start, set to true #for debug set to true initially

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(self.MQTT_TOPIC)

    def on_message(self, client, userdata, msg):
        json_data = json.loads(msg.payload)
        tp = json_data["type"].lower()

        if tp == "start":
            json_data["cur_day"] = self.cur_day
            self.daytime = True
            self.cur_day += 1
        elif tp == "end":
            self.daytime = False

        # Put the received message into the queue
        # if self.daytime:
        self.queue.put(json_data)

    def listen(self):
        client = mqtt.Client(client_id=self.CLIENT_ID, clean_session=True)
        client.username_pw_set(self.MQTT_USERNAME, self.MQTT_PASSWORD)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.MQTT_BROKER, self.MQTT_PORT, 60)
        client.loop_forever()

class Processor:
    truck_cols = ['seq', 'type', 'truckId', 'positionLatitude', 'positionLongitude', 'equipType', 'nextTripLengthPreference',
        "hour","minute","day_of_week","is_weekend"]
    load_cols = ['seq', 'type', 'loadId', 'originLatitude', 'originLongitude', 'destinationLatitude', 'destinationLongitude', 'equipmentType', 'price', 'mileage',
        "hour","minute","day_of_week","is_weekend"]

    def __init__ (self):
        self._start()


    def _start(self):
        # Reset DataFrames for new day
        self.truck_df = pd.DataFrame(columns=Processor.truck_cols)
        self.load_df = pd.DataFrame(columns=Processor.load_cols)

        #Used to store memory, This should be new every day.
        # What is the difference between this and the dfs above?
        # Maybe we want to change the trucks_df to a trucks dict
        self.truck_map = {}


    # Define a function to process messages from the queue and update DataFrames
    def process_data(self,
                    message_queue: queue.Queue,
                    ) -> Tuple[pd.DataFrame, pd.DataFrame, bool]:

        # df for load
        # dict for trucks
        #     have a field that calcs vals for all loads
        #actually do this part later
        # process then add to those mems

        # pop from queue one at a time.

        while and not message_queue.empty():
            json_data = message_queue.get()

            # Create a temp df to hold your new payload
            # Split time format from payload into its components (hour, minute, etc)
            temp_df = Processor.preprocess_time(pd.DataFrame.from_dict(json_data, orient='index').T)

            # Type of the message (truck, load, start, or end)
            tp = temp_df['type'].item().lower()

            if tp == 'start':
                #This will basically reset the dfs
                print('Start of day')
                self._start()

            elif tp == 'truck':
                print('Trucks:', temp_df['truckId'])
                self.truck_df = pd.concat([self.truck_df, temp_df], ignore_index=True)

            elif tp == 'load':
                print('Loads:', temp_df['loadId'])
                self.load_df = pd.concat([self.load_df, temp_df], ignore_index=True)
            elif tp == 'end':

                #return df
                print("End of day")
                return self.truck_df, self.load_df, True


        # Return DataFrames in case they need to be used immediately after calling
        return self.truck_df, self.load_df, False

    @staticmethod
    def preprocess_time (df: pd.DataFrame):
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['minute'] = df['timestamp'].dt.minute
            df['day_of_week'] = df['timestamp'].dt.dayofweek
            df['is_weekend'] = df['timestamp'].dt.weekday.isin([5, 6]).astype(int)

            df = df.drop(columns=['timestamp'])
        except:
            print (df)
            raise TypeError
        return df

    def _calculate_scores(self, truck_id):
        # Add to the dict, which will update the position of the truck
        # and figure out if the truck is new by using a flag?
        # No, just calculate the score the truck with the new position
        # needs to assign to all the loads near it
        pass


# Define global DataFrames
# truck_df = pd.DataFrame()
# load_df = pd.DataFrame()
if __name__ == "__main__":
    import threading
    import time
    processor = Processor()
    def batch_process_data():
        print("Commencing batch processing")
        while True:
            print (q)
            if not q.empty():
                truck_data, load_data, eod = processor.process_data(q)

                if not truck_data.empty:
                    print (f'Truck Data\n\n{(truck_data).head(5)}')
                if not load_data.empty:
                    print (f'Truck Data\n\n{(load_data).head(5)}')

            time.sleep(5)  # Process every 5 seconds


    q = queue.Queue()
    handler = MqttHandler(q)
    listener_thread = threading.Thread(target=handler.listen)
    processor_thread = threading.Thread(target=batch_process_data)

    listener_thread.start()
    processor_thread.start()
