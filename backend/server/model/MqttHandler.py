import paho.mqtt.client as mqtt
import json
from queue import Queue
from typing import Any, Dict

class MqttHandler:
    # MQTT Settings
    MQTT_BROKER: str = "fortuitous-welder.cloudmqtt.com"  # MQTT broker address
    MQTT_PORT: int = 1883  # MQTT broker port
    MQTT_TOPIC: str = "CodeJam"  # MQTT topic to subscribe to
    MQTT_USERNAME: str = "CodeJamUser"  # MQTT username for authentication
    MQTT_PASSWORD: str = "123CodeJam"  # MQTT password for authentication
    CLIENT_ID: str = "GDSC01"  # MQTT client ID, replace with your team name

    def __init__(self, message_queue: Queue):
        """
        Initialize the MQTT handler.

        Args:
            message_queue (Queue): A queue to store received MQTT messages.
        """
        self.queue = message_queue  # Store the provided message queue
        self.cur_day: int = 0  # Initialize a variable to keep track of the current day

    def on_connect(self, client: mqtt.Client, userdata: Any, flags: Dict[str, Any], rc: int) -> None:
        """
        Callback function called when the MQTT client connects to the broker.

        Args:
            client (mqtt.Client): The MQTT client instance.
            userdata (Any): User data (not used in this example).
            flags (Dict[str, Any]): Connection flags (not used in this example).
            rc (int): Connection result code.
        """
        print("Connected with result code " + str(rc))
        client.subscribe(self.MQTT_TOPIC)  # Subscribe to the specified MQTT topic

    def on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
        """
        Callback function called when a new MQTT message is received.

        Args:
            client (mqtt.Client): The MQTT client instance.
            userdata (Any): User data (not used in this example).
            msg (mqtt.MQTTMessage): MQTT message object containing payload and topic information.
        """
        json_data: Dict[str, Any] = json.loads(msg.payload)  # Parse the received JSON payload

        if json_data["type"].lower() == "start":
            json_data["cur_day"] = self.cur_day
            self.cur_day += 1

        # Put the received message into the queue for further processing
        self.queue.put(json_data)

        # Example to print queue contents (uncomment to see the contents)
        # print(list(self.queue.queue))

    def listen(self) -> None:
        """
        Start listening for MQTT messages and subscribe to the specified topic.
        """
        client: mqtt.Client = mqtt.Client(client_id=self.CLIENT_ID, clean_session=True)
        client.username_pw_set(self.MQTT_USERNAME, self.MQTT_PASSWORD)
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        # Connect to the MQTT broker and start the message loop
        client.connect(self.MQTT_BROKER, self.MQTT_PORT, 60)
        client.loop_forever()
