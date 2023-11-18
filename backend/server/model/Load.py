import pandas as pd

class Load:
    def __init__(self, ID, price, mileage, equipment_type, oLatitude, oLongitude, dLatitude, dLongitude):
        self.id = ID
        self.price = price
        self.mileage = mileage
        self.equipment_type = equipment_type
        self.destination = (dLatitude, dLongitude)

        self.origin = (oLatitude, oLongitude)

    @classmethod
    def createLoads(cls, df):
        pass
