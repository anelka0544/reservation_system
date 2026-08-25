import pytest
from clients.fake_repositories import FakeUserRepository
from controllers.user_controller import UserController
from shared.exceptions import WrongUserEmail

@pytest.mark.asyncio
async def test_create_user_ok():
    repo = FakeUserRepository()
    ctrl = UserController(repo)
    u = await ctrl.create_user("alex", "alex@mail.com", "qwerty", False)
    assert u.user_id == 1
    assert u.name == "alex"

@pytest.mark.asyncio
async def test_create_user_dup():
    repo = FakeUserRepository()
    ctrl = UserController(repo)
    await ctrl.create_user("alex", "alex@mail.com", "qwerty", False)
    with pytest.raises(WrongUserEmail):
        await ctrl.create_user("qq", "alex@mail.com", "123", False)

@pytest.mark.asyncio
async def test_auth():
    repo = FakeUserRepository()
    ctrl = UserController(repo)
    await ctrl.create_user("ann", "ann@mail.com", "qwerty", False)

    u = await ctrl.authenticate_user("ann@mail.com", "qwerty")
    assert u is not None

    bad_u = await ctrl.authenticate_user("ann@mail.com", "123123")
    assert bad_u is None