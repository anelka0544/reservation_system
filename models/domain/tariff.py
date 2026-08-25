class Tariff:
    def __init__(self, hourly_rate:float, daily_rate:float, monthly_rate:float, tariff_id: int|None = None):
        self.tariff_id = tariff_id
        self.hourly_rate = hourly_rate
        self.daily_rate = daily_rate
        self.monthly_rate = monthly_rate