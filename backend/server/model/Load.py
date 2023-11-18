import pandas as pd

class Load:
    def __init__(self, price, mileage, equipment_type, origin, destination):
        self.price = price
        self.mileage = mileage
        self.equipment_type = equipment_type
        self.origin = origin
        self.destination = destination

    @classmethod
    def createLoads(cls, df):
        pass