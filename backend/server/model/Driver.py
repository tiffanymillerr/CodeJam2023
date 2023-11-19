import pandas as pd

class Driver:
    def __init__(self, ID, lLatitude, lLongitude, equip_type, trip_length_preference, hour, minute, day_of_week, is_weekend):
        self.id = ID
        self.equip_type = equip_type
        self.trip_length_preference = trip_length_preference

        self.location = (lLatitude, lLongitude)
        self.hour = hour
        self.minute = minute
        self.day_of_week = day_of_week
        self.is_weekend = is_weekend

    @classmethod
    def buildInstanceFromSeries(cls, row: pd.Series):
        # Extract values from the Series
        driver_id = row['truckId']
        equip_type = row['equipType']
        trip_length_preference = row['nextTripLengthPreference']
        l_latitude = row['positionLatitude']
        l_longitude = row['positionLongitude']
        hour = row['hour']
        minute = row['minute']
        day_of_week = row['day_of_week']
        is_weekend = row['is_weekend']

        # Create and return an instance of the Driver class
        return cls(driver_id, l_latitude, l_longitude, equip_type, trip_length_preference, hour, minute, day_of_week, is_weekend)

