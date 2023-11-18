from fastapi import FastAPI

app = FastAPI()

START_TIME = -1
END_TIME = -1

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}

@app.get("/score/{loadID}")
def getScoreFromLoadID(loadID: int):
    
    return score(loadID)


def score(loadID):
    return 1000

def minScore():
    pass

def onStartEvent(time):
    # START_TIME = time
    # END_TIME = time + 5min
    pass

def onLoadEvent():
    pass

class Load():
    pass

class Truck():

    def __init__(self, id):

        # Query the server database for truck with ID=id
        pass

    def accept(self, load):
        pass