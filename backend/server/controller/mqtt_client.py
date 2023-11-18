import csv
import json
import os
import paho.mqtt.client as mqtt
from datetime import datetime
import pandas as pd

# MQTT Settings
MQTT_BROKER = "fortuitous-welder.cloudmqtt.com"
MQTT_PORT = 1883
MQTT_TOPIC = "CodeJam"
MQTT_USERNAME = "CodeJamUser"
MQTT_PASSWORD = "123CodeJam"
CLIENT_ID = "GDSC01"

# Output Format and Folder Settings
OUTPUT_FORMAT = "csv"  # Change to "json" for JSON output
OUTPUT_FOLDER = "mqtt_data"
MAX_FILES_PER_DATE = 10
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

class MqttHandler:
    def __init__(self):
        self.truck = pd.DataFrame(columns=['seq', 'type', 'timestamp', 'truckId', 'positionLatitude', 'positionLongitude', 'equipType', 'nextTripLengthPreference'])
        self.load = pd.DataFrame(columns=['seq', 'type', 'timestamp', 'loadId', 'originLatitude', 'originLongitude', 'destinationLatitude', 'destinationLongitude', 'equipmentType', 'price', 'mileage'])
        self.cur_day = 0
    
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(MQTT_TOPIC)

    def on_message(self, client, userdata, msg):
        json_data = json.loads(msg.payload)

        # Convert Python object to Pandas DataFrame
        temp_df = pd.DataFrame.from_dict(json_data, orient='index').T
        tp = temp_df['type'].item()
        
        if tp == 'Start':
            self.truck = pd.DataFrame(columns=['seq', 'type', 'timestamp', 'truckId', 'positionLatitude', 'positionLongitude', 'equipType', 'nextTripLengthPreference'])
            self.load = pd.DataFrame(columns=['seq', 'type', 'timestamp', 'loadId', 'originLatitude', 'originLongitude', 'destinationLatitude', 'destinationLongitude', 'equipmentType', 'price', 'mileage'])
            print("Start of new day")
            self.cur_day += 1
        elif self.truck is not None and self.load is not None:
            if tp == 'Truck':
                print("Got truck")
                self.truck = pd.concat([self.truck, temp_df])
                #self.truck.append(temp_df, ignore_index=True)
            elif tp == 'Load':
                print("Got load")
                self.load = pd.concat([self.load, temp_df])
                #self.load.append(temp_df, ignore_index=True)
            elif tp == 'End':
                print("End of day")
                self.truck.to_csv(f'mqtt_data_2/truck_{self.cur_day}.csv', index=False)
                self.load.to_csv(f'mqtt_data_2/load_{self.cur_day}.csv', index=False)

                self.truck = None
                self.load = None
        else:
            print("Got message, not start of day")

# Create an MQTT client and attach the callback functions
client = mqtt.Client(client_id=CLIENT_ID, clean_session=True)
client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
handler = MqttHandler()
client.on_connect = handler.on_connect
client.on_message = handler.on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the loop
client.loop_forever()
