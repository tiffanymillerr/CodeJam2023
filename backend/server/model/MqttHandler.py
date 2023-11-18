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
    
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(self.MQTT_TOPIC)

    def on_message(self, client, userdata, msg):
        json_data = json.loads(msg.payload)

        if json_data["type"].lower() == "start":
            json_data["cur_day"] = self.cur_day
            self.cur_day += 1

        # Put the received message into the queue
        self.queue.put(json_data)

        # Example to print queue contents
        print(list(self.queue.queue))

    def listen(self):
        client = mqtt.Client(client_id=self.CLIENT_ID, clean_session=True)
        client.username_pw_set(self.MQTT_USERNAME, self.MQTT_PASSWORD)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.MQTT_BROKER, self.MQTT_PORT, 60)
        client.loop_forever()

if __name__ == '__main__':
    handler = MqttHandler()
    handler.listen()
