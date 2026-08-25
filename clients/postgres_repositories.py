from datetime import datetime
from typing import Generic, TypeVar, List, Optional
import asyncpg

from models.abstractions.interfaces import ILocationRepository, IBookingRepository, IUserRepository, IWorkspaceRepository, ITariffRepository
from models.domain.booking import Booking
from models.domain.workspace import Workspace, WorkspaceType
from models.domain.user import User
from models.domain.location import Location
from models.domain.tariff import Tariff

class PostgresBookingRepo(IBookingRepository):
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def create(self, booking: Booking) -> Booking:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "insert into bookings (user_id, workspace_id, from_time, to_time, total_price, status) values ($1, $2, $3, $4, $5, $6) returning booking_id",
                booking.user_id, booking.workspace_id, booking.from_time, booking.to_time, booking.total_price, booking.status
            )
            booking.booking_id = row["booking_id"]
            return booking

    async def get_all(self) -> list[Booking]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("select * from bookings")
            return [self._to_entity(r) for r in rows]
        
    async def get_by_id(self, booking_id: int) -> Booking | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow("select * from bookings where booking_id = $1", booking_id)
            return self._to_entity(row) if row else None

    async def update(self, booking: Booking) -> Booking | None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                "update bookings set user_id=$1, workspace_id=$2, from_time=$3, to_time=$4, total_price=$5, status=$6 where booking_id=$7",
                booking.user_id, booking.workspace_id, booking.from_time, booking.to_time, booking.total_price, booking.status, booking.booking_id
            )
            return booking

    async def delete(self, booking_id: int) -> bool:
        async with self._pool.acquire() as conn:
            result = await conn.execute("delete from bookings where booking_id = $1", booking_id)
            return result == "DELETE 1"
        
    async def is_workspace_available(self, workspace_id: int, start: datetime, end: datetime) -> bool:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "select count(*) as booked from bookings where workspace_id = $1 and status = 'active' and (from_time, to_time) overlaps ($2, $3)",
                workspace_id, start, end
            )
            return row["booked"] == 0      

    def _to_entity(self, row) -> Booking:
        booking = Booking(
            user_id=row["user_id"], 
            workspace_id=row["workspace_id"], 
            from_time=row["from_time"], 
            to_time=row["to_time"], 
            total_price=row["total_price"], 
            status=row["status"]
        )
        booking.booking_id = row["booking_id"]
        return booking


class PostgresWorkspaceRepository(IWorkspaceRepository):
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def create(self, workspace: Workspace) -> Workspace:
        async with self._pool.acquire() as conn:
            ws_type = workspace.workspace_type.value if isinstance(workspace.workspace_type, WorkspaceType) else workspace.workspace_type
            row = await conn.fetchrow(
                "insert into workspaces (name, location_id, tariff_id, workspace_type) values ($1, $2, $3, $4) returning workspace_id",
                workspace.name, workspace.location_id, workspace.tariff_id, ws_type
            )
            workspace.workspace_id = row["workspace_id"]
            return workspace

    async def get_all(self) -> list[Workspace]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("select * from workspaces")
            return [self._to_entity(r) for r in rows]
        
    async def get_by_id(self, workspace_id: int) -> Workspace | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow("select * from workspaces where workspace_id = $1", workspace_id)
            return self._to_entity(row) if row else None

    async def update(self, workspace: Workspace) -> Workspace | None:
        async with self._pool.acquire() as conn:
            ws_type = workspace.workspace_type.value if isinstance(workspace.workspace_type, WorkspaceType) else workspace.workspace_type
            await conn.execute(
                "update workspaces set name=$1, location_id=$2, tariff_id=$3, workspace_type=$4 where workspace_id=$5",
                workspace.name, workspace.location_id, workspace.tariff_id, ws_type, workspace.workspace_id
            )
            return workspace

    async def delete(self, workspace_id: int) -> bool:
        async with self._pool.acquire() as conn:
            result = await conn.execute("delete from workspaces where workspace_id = $1", workspace_id)
            return result == "DELETE 1"

    async def get_workspaces_by_location(self, location_id: int, workspace_type: Optional[WorkspaceType] = None) -> list[Workspace]:
        async with self._pool.acquire() as conn:
            if workspace_type:
                ws_type = workspace_type.value if isinstance(workspace_type, WorkspaceType) else workspace_type
                rows = await conn.fetch(
                    "select * from workspaces where location_id = $1 and workspace_type = $2",
                    location_id, ws_type
                )
            else:
                rows = await conn.fetch(
                    "select * from workspaces where location_id = $1",
                    location_id
                )
            return [self._to_entity(r) for r in rows]

    def _to_entity(self, row) -> Workspace:
        ws = Workspace(
            name=row["name"], 
            location_id=row["location_id"], 
            tariff_id=row["tariff_id"], 
            workspace_type=WorkspaceType(row["workspace_type"]) 
        )
        ws.workspace_id = row["workspace_id"]
        return ws


class PostgresUserRepository(IUserRepository):
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def create(self, user: User) -> User:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "insert into users (name, mail, hash_password, is_admin) values ($1, $2, $3, $4) returning user_id",
                user.name, user.mail, user.hash_password, user.is_admin
            )
            user.user_id = row["user_id"]
            return user

    async def get_by_email(self, email: str) -> User | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow("select * from users where mail = $1", email)
            return self._to_entity(row) if row else None

    async def get_by_id(self, user_id: int) -> User | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow("select * from users where user_id = $1", user_id)
            return self._to_entity(row) if row else None

    async def update(self, user: User) -> User | None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                "update users set name=$1, mail=$2, hash_password=$3, is_admin=$4 where user_id=$5",
                user.name, user.mail, user.hash_password, user.is_admin, user.user_id
            )
            return user

    async def delete(self, user_id: int) -> bool:
        async with self._pool.acquire() as conn:
            result = await conn.execute("delete from users where user_id = $1", user_id)
            return result == "DELETE 1"

    def _to_entity(self, row) -> User:
        user = User(
            name=row["name"],
            mail=row["mail"],
            hash_password=row["hash_password"],
            is_admin=row["is_admin"]
        )
        user.user_id = row["user_id"]
        return user


class PostgresLocationRepository(ILocationRepository):
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def create(self, location: Location) -> Location:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "insert into locations (city, street, building) values ($1, $2, $3) returning location_id",
                location.city, location.street, location.building
            )
            location.location_id = row["location_id"]
            return location

    async def get_all(self) -> list[Location]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("select * from locations")
            return [self._to_entity(r) for r in rows]

    async def get_by_id(self, location_id: int) -> Location | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow("select * from locations where location_id = $1", location_id)
            return self._to_entity(row) if row else None

    async def update(self, location: Location) -> Location | None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                "update locations set city=$1, street=$2, building=$3 where location_id=$4",
                location.city, location.street, location.building, location.location_id
            )
            return location

    async def delete(self, location_id: int) -> bool:
        async with self._pool.acquire() as conn:
            result = await conn.execute("delete from locations where location_id = $1", location_id)
            return result == "DELETE 1"

    def _to_entity(self, row) -> Location:
        loc = Location(
            city=row["city"],
            street=row["street"],
            building=row["building"]
        )
        loc.location_id = row["location_id"]
        return loc
    
class PostgresTariffRepository(ITariffRepository):
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def create(self, tariff: Tariff) -> Tariff:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "insert into tariffs (hourly_rate, daily_rate, monthly_rate) values ($1, $2, $3) returning tariff_id",
                tariff.hourly_rate, tariff.daily_rate, tariff.monthly_rate
            )
            tariff.tariff_id = row["tariff_id"]
            return tariff

    async def get_all(self) -> list[Tariff]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("select * from tariffs")
            return [self._to_entity(r) for r in rows]

    async def get_by_id(self, tariff_id: int) -> Tariff | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow("select * from tariffs where tariff_id = $1", tariff_id)
            return self._to_entity(row) if row else None

    async def update(self, tariff: Tariff) -> Tariff | None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                "update tariffs set hourly_rate=$1, daily_rate=$2, monthly_rate=$3 where tariff_id=$4",
                tariff.hourly_rate, tariff.daily_rate, tariff.monthly_rate, tariff.tariff_id
            )
            return tariff

    async def delete(self, tariff_id: int) -> bool:
        async with self._pool.acquire() as conn:
            result = await conn.execute("delete from tariffs where tariff_id = $1", tariff_id)
            return result == "DELETE 1"

    def _to_entity(self, row) -> Tariff:
        tr = Tariff(
            hourly_rate=row["hourly_rate"],
            daily_rate=row["daily_rate"],
            monthly_rate=row["monthly_rate"]
        )
        tr.tariff_id = row["tariff_id"]
        return tr