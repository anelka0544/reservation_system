from datetime import datetime
from models.abstractions.interfaces import ITariffRepository
from models.domain.tariff import Tariff

class TariffController:
    def __init__(self, tariff_repo: ITariffRepository):
        self.tariff_repo = tariff_repo

    async def create_tariff(self, hourly_rate: float, daily_rate:float, monthly_rate:float) -> Tariff:
        new_ = Tariff(hourly_rate=hourly_rate, daily_rate=daily_rate, monthly_rate=monthly_rate)
        saved_ = await self.tariff_repo.create(new_)
        return saved_
    
    async def get_all_(self) -> list[Tariff]:
        return await self.tariff_repo.get_all()