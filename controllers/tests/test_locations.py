import pytest
from clients.fake_repositories import FakeLocationRepository, FakeWorkspaceRepository, FakeBookingRepo
from controllers.location_contoller import LocationController
from shared.exceptions import LocationNotFoundError

@pytest.mark.asyncio
async def test_create_loc():
    l_repo = FakeLocationRepository()
    w_repo = FakeWorkspaceRepository()
    b_repo = FakeBookingRepo()
    ctrl = LocationController(l_repo, w_repo, b_repo)
    loc = await ctrl.create_location("Minsk", "Kirova", 15)
    assert loc.location_id == 1
    assert loc.city == "Minsk"

@pytest.mark.asyncio
async def test_get_all_locs():
    l_repo = FakeLocationRepository()
    ctrl = LocationController(l_repo, FakeWorkspaceRepository(), FakeBookingRepo())
    await ctrl.create_location("Minsk", "Kirova", 15)
    await ctrl.create_location("Brest", "Lenina", 1)
    locs = await ctrl.get_all_locations()
    assert len(locs) == 2

@pytest.mark.asyncio
async def test_stats_not_found():
    l_repo = FakeLocationRepository()
    ctrl = LocationController(l_repo, FakeWorkspaceRepository(), FakeBookingRepo())
    with pytest.raises(LocationNotFoundError):
        await ctrl.get_location_load_stats(999)