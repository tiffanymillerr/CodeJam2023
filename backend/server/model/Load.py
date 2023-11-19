import pandas as pd
from Driver from Driver

class Load:
    def __init__(self, ID, price, mileage, equipment_type, oLatitude, oLongitude, dLatitude, dLongitude):
        self.id = ID
        self.price = price
        self.mileage = mileage
        self.equipment_type = equipment_type
        self.destination = (dLatitude, dLongitude)

        self.origin = (oLatitude, oLongitude)

        self.msg = {}

    @classmethod
    def buildInstanceFromSeries(cls, row: pd.Series):
        # Extract values from the Series
        load_id = row['loadId']
        price = row['price']
        mileage = row['mileage']
        equipment_type = row['equipmentType']
        o_latitude = row['originLatitude']
        o_longitude = row['originLongitude']
        d_latitude = row['destinationLatitude']
        d_longitude = row['destinationLongitude']

        # Create and return an instance of the Load class
        return cls(load_id, price, mileage, equipment_type, o_latitude, o_longitude, d_latitude, d_longitude)

