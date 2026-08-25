from datetime import datetime

class Booking:
    def __init__(self, user_id: int, workspace_id: int, from_time: datetime, to_time: datetime, status: str, total_price: int, booking_id: int|None = None):
        self.user_id = user_id
        self.workspace_id = workspace_id
        self.booking_id = booking_id
        self.from_time = from_time
        self.to_time = to_time
        self.total_price = total_price
        self.status = status