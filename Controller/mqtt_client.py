import csv
import json
import os
import paho.mqtt.client as mqtt
from datetime import datetime
import find_path
from typing import Optional, IO, Any, Dict

# Find the project root
project_root = find_path.get_project_root(
    find_path.os.path.dirname(
        find_path.os.path.abspath(__file__)
        )
    )

# Load configurations from config.json
config_path = os.path.join(project_root, 'config.json')
with open('config.json') as config_file:
    config = json.load(config_file)

# MQTT Settings
MQTT_BROKER = config['mqtt']['broker']
MQTT_PORT = config['mqtt']['port']
MQTT_TOPIC = config['mqtt']['topic']
MQTT_USERNAME = config['mqtt']['username']
MQTT_PASSWORD = config['mqtt']['password']
CLIENT_ID = config['mqtt']['client_id']

# Output Format and Folder Settings
OUTPUT_FORMAT = config['output']['format']
MAX_FILES_PER_DATE = config['output']['max_files_per_date']

OUTPUT_FOLDER = os.path.join(project_root, config['output']['folder'])
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Global variables
current_file: Optional[IO[str]] = None
file_counters: Dict[str, int] = {}

# Function to open a new file for the given date
def open_new_file(date_str:str) -> Optional[IO[str]]:
    # Increment the counter for this date
    file_counters[date_str] = file_counters.get(date_str, 0) + 1
    if file_counters[date_str] > MAX_FILES_PER_DATE:
        print(f"Maximum number of files reached for {date_str}. No new file will be created.")
        return None

    # Create file name with counter
    counter_str = f"_{file_counters[date_str]:04d}" if file_counters[date_str] > 1 else ""
    file_name = f"mqtt_data_{date_str}{counter_str}.{OUTPUT_FORMAT}"
    file_path = os.path.join(OUTPUT_FOLDER, file_name)
    
    file = open(file_path, 'w', newline='', encoding='utf-8')
    if OUTPUT_FORMAT == "json":
        json.dump([], file)  # Initialize with an empty list
    return file

# Callback for when the client receives a CONNACK response from the server
def on_connect(client: mqtt.Client, userdata: Any, flags: Dict, rc: int) -> None:
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

# Callback for when a PUBLISH message is received from the server
def on_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
    global current_file

    print(f"Message received on topic {msg.topic}")

    # Convert message payload to a Python dictionary
    message_data = json.loads(msg.payload)

    # Handle Start event
    if message_data["type"] == "Start":
        date_str = datetime.fromisoformat(message_data["timestamp"]).strftime("%Y-%m-%d")
        if current_file is not None:
            current_file.close()
        current_file = open_new_file(date_str)

    # Write data to file for other message types
    elif current_file is not None and message_data["type"] != "End":
        if OUTPUT_FORMAT == "csv":
            writer = csv.writer(current_file)
            writer.writerow([message_data.get(key, '') for key in sorted(message_data)])
        elif OUTPUT_FORMAT == "json":
            current_file.seek(0)
            data = json.load(current_file)
            data.append(message_data)
            current_file.seek(0)
            current_file.truncate()
            json.dump(data, current_file)

# Create an MQTT client and attach the callback functions
client = mqtt.Client(client_id=CLIENT_ID, clean_session=True)
client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the loop
client.loop_forever()
