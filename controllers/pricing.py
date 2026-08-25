from abc import ABC, abstractmethod
from datetime import timedelta
import math
from models.domain.tariff import Tariff

class PriceCalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, tariff: Tariff, duration: timedelta) -> float:
        pass

class HourlyStrategy(PriceCalculationStrategy):
    def calculate(self, tariff: Tariff, duration: timedelta) -> float:
        hours = duration.total_seconds() / 3600
        return math.ceil(hours) * tariff.hourly_rate

class DailyStrategy(PriceCalculationStrategy):
    def calculate(self, tariff: Tariff, duration: timedelta) -> float:
        days = duration.total_seconds() / (3600 * 24)
        return math.ceil(days) * tariff.daily_rate
    
class MonthlyStrategy(PriceCalculationStrategy):
    def calculate(self, tariff: Tariff, duration: timedelta) -> float:
        month = duration.total_seconds() / (3600 * 24 * 30)
        return math.ceil(month) * tariff.monthly_rate

class PriceCalculator:
    def calculate_price(self, tariff: Tariff, duration: timedelta) -> float:
        hours = duration.total_seconds() / 3600
        
        if hours < 24:
            strategy = HourlyStrategy()
        elif hours < 720: 
            strategy = DailyStrategy()
        else:
            strategy = MonthlyStrategy() 

        return strategy.calculate(tariff, duration)