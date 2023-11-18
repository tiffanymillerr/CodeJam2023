class Load:
    def __init__(self, ID, price, mileage, equipment_type, oLatitude, oLongitude, destination):
        self.id = ID
        self.price = price
        self.mileage = mileage
        self.equipment_type = equipment_type
        self.destination = destination

        self.origin = (oLatitude, oLongitude)