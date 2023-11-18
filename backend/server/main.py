from fastapi import FastAPI
from controller.connector import MqttHandler, process_data
from model.Score import onLoadEvent
import queue, threading

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/truck")
def list_trucks():
    # Return list of all truck IDs
    pass

@app.get("/truck/{id}/notifications")
def get_notifications_for_truck(id: int):
    # Return a list of all the notifications the trucker has gotten
    return NOTIF.get(id)

if __name__ == '__main__':
    # Thread-Safe Queue
    message_queue = queue.Queue()

    # Set Up Handler
    handler = MqttHandler(message_queue)

    # Threads Setup
    listener_thread = threading.Thread(target=handler.listen)

    # Start Listener Thread
    listener_thread.start()

    # Example usage of process_data function
    NOTIF = {}      # might cause issues where its declared
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

                for new_load in load_data:
                    for driver in allDrivers:
                        # current_time = (hour, minute, day_of_week, is_weekend)
                        if onLoadEvent(new_load, current_time, driver):     # on load event returns a load if you should be notified (None otherwise)
                            if NOTIF.get(driver.id) is None:
                                NOTIF[driver.id] = [new_load]
                            else:
                                NOTIF[driver.id].append(new_load)


            time.sleep(5)  # Process every 5 seconds

    # Start periodic processing in a separate thread
    processor_thread = threading.Thread(target=periodically_process_data)
    processor_thread.start()