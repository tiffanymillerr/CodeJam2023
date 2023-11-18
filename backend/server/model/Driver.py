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