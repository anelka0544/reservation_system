class Location:
    def __init__(self, city: str, street: str, building: int, location_id: int|None = None):
        self.location_id = None
        self.city = city
        self.street = street
        self.building = building