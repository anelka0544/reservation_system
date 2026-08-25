import pytest
from datetime import datetime, timedelta
from clients.fake_repositories import FakeBookingRepo, FakeWorkspaceRepository, FakeUserRepository, FakeTariffRepo
from models.abstractions.interfaces import ITariffRepository
from controllers.booking_controller import BookingController
from controllers.pricing import PriceCalculator
from models.domain.user import User
from models.domain.workspace import Workspace, WorkspaceType
from models.domain.tariff import Tariff
from shared.exceptions import InvalidTimeError, WorkspaceAlreadyBookedError

# pytest --cov=.

@pytest.mark.asyncio
async def test_create_booking_success():
    b_repo = FakeBookingRepo()
    w_repo = FakeWorkspaceRepository()
    u_repo = FakeUserRepository()
    t_repo = FakeTariffRepo()
    calc = PriceCalculator()
    
    ctrl = BookingController(b_repo, w_repo, calc, u_repo, t_repo)
    
    await u_repo.create(User("Test", "test@test.com", "hash", False))
    await t_repo.create(Tariff(100, 1000, 5000))
    await w_repo.create(Workspace("Desk 1", 1, 1, WorkspaceType.DESK))
    
    start = datetime(2026, 1, 1, 10, 0)
    end = datetime(2026, 1, 1, 12, 0) 
    
    bk = await ctrl.create_booking(1, 1, start, end)
    
    assert bk.booking_id == 1
    assert bk.total_price == 200
    assert bk.status == "Active"

@pytest.mark.asyncio
async def test_create_booking_invalid_time():
    ctrl = BookingController(FakeBookingRepo(), FakeWorkspaceRepository(), PriceCalculator(), FakeUserRepository(), FakeTariffRepo())
    
    start = datetime(2026, 1, 1, 12, 0)
    end = datetime(2026, 1, 1, 10, 0) 
    
    with pytest.raises(InvalidTimeError):
        await ctrl.create_booking(1, 1, start, end)

@pytest.mark.asyncio
async def test_workspace_already_booked():
    b_repo = FakeBookingRepo()
    w_repo = FakeWorkspaceRepository()
    u_repo = FakeUserRepository()
    t_repo = FakeTariffRepo()
    
    ctrl = BookingController(b_repo, w_repo, PriceCalculator(), u_repo, t_repo)
    
    await u_repo.create(User("Test", "test@test.com", "hash", False))
    await t_repo.create(Tariff(100, 1000, 5000))
    await w_repo.create(Workspace("Desk 1", 1, 1, WorkspaceType.DESK))
    
    start = datetime(2026, 1, 1, 10, 0)
    end = datetime(2026, 1, 1, 12, 0)

    await ctrl.create_booking(1, 1, start, end)
    
    with pytest.raises(WorkspaceAlreadyBookedError):
        await ctrl.create_booking(1, 1, start, end)