import csv
import json
import os
import paho.mqtt.client as mqtt
from datetime import datetime

# MQTT Settings
MQTT_BROKER = "fortuitous-welder.cloudmqtt.com"
MQTT_PORT = 1883
MQTT_TOPIC = "CodeJam"
MQTT_USERNAME = "CodeJamUser"
MQTT_PASSWORD = "123CodeJam"
CLIENT_ID = "GDSC01"  # Replace with your team name

# Output Format and Folder Settings
OUTPUT_FORMAT = "csv"  # Change to "json" for JSON output
OUTPUT_FOLDER = "mqtt_data"
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Global variable to keep track of the current file and date
current_file = None
current_date = None

# Function to open a new file for the current date
def open_new_file(date_str):
    file_name = f"mqtt_data_{date_str}.{OUTPUT_FORMAT}"
    file_path = os.path.join(OUTPUT_FOLDER, file_name)
    file = open(file_path, 'w', newline='', encoding='utf-8')
    if OUTPUT_FORMAT == "json":
        json.dump([], file)  # Initialize with an empty list
    return file

# Callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

# Callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    global current_file, current_date

    print(f"Message received on topic {msg.topic}")

    # Convert message payload to a Python dictionary
    message_data = json.loads(msg.payload)

    # Extract the date from the Start event and open a new file
    if message_data["type"] == "Start":
        date_str = datetime.fromisoformat(message_data["timestamp"]).strftime("%Y-%m-%d")
        if date_str != current_date:
            if current_file is not None:
                current_file.close()
            current_file = open_new_file(date_str)
            current_date = date_str

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
