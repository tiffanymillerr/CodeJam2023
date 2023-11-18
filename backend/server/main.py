from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/truck")
def list_trucks():
    # Return list of all truck IDs
    pass

@app.get("/truck/{id}/notifications")
def get_notifications_for_truck():
    # Return a list of all the notifications the trucker has gotten
    pass