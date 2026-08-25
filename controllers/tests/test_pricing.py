import pytest
from datetime import timedelta
from controllers.pricing import PriceCalculator
from models.domain.tariff import Tariff

def test_hourly_price():
    calc = PriceCalculator()
    t = Tariff(100, 1000, 5000)
    res = calc.calculate_price(t, timedelta(hours=2.5))
    assert res == 300 

def test_daily_price():
    calc = PriceCalculator()
    t = Tariff(100, 1000, 5000)
    res = calc.calculate_price(t, timedelta(hours=25))
    assert res == 2000

def test_monthly_price():
    calc = PriceCalculator()
    t = Tariff(100, 1000, 5000)
    res = calc.calculate_price(t, timedelta(days=35))
    assert res == 10000