#from clients.fake_repositories import FakeUserRepository, FakeBookingRepo, FakeLocationRepository, FakeWorkspaceRepository
from clients.postgres_repositories import PostgresBookingRepo, PostgresLocationRepository, PostgresUserRepository, PostgresWorkspaceRepository, PostgresTariffRepository
from controllers.user_controller import UserController
from controllers.booking_controller import BookingController
from controllers.location_contoller import LocationController
from controllers.workspace_controller import WorkspaceController
from controllers.tariff_controller import TariffController
from controllers.pricing import PriceCalculator
from clients.database.connection import get_pool

price_calculator = PriceCalculator()

async def get_user_controller() -> UserController:
    pool = await get_pool()
    return UserController(PostgresUserRepository(pool))

async def get_workspace_controller() -> WorkspaceController:
    pool = await get_pool()
    return WorkspaceController(PostgresWorkspaceRepository(pool), PostgresBookingRepo(pool), PostgresLocationRepository(pool), PostgresTariffRepository(pool))

async def get_location_controller() -> LocationController:
    pool = await get_pool()
    return LocationController(PostgresLocationRepository(pool), PostgresWorkspaceRepository(pool), PostgresBookingRepo(pool))

async def get_booking_controller() -> BookingController:
    pool = await get_pool()
    return BookingController(PostgresBookingRepo(pool), PostgresWorkspaceRepository(pool), price_calculator, PostgresUserRepository(pool), PostgresTariffRepository(pool))

async def get_tariff_controller() -> TariffController:
    pool = await get_pool()
    return TariffController(PostgresTariffRepository(pool))