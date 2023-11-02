import json
from uuid import uuid4

import pytest

from db.models import PortalRole
from tests.conftest import create_test_auth_headers_for_user

MSG = "value is not a valid email address: The email address is not valid. It must have exactly one @-sign."


@pytest.mark.parametrize(
    "user_roles",
    (
        [PortalRole.ROLE_PORTAL_SUPERADMIN],
        [PortalRole.ROLE_PORTAL_ADMIN],
        [PortalRole.ROLE_PORTAL_USER],
        [PortalRole.ROLE_PORTAL_USER, PortalRole.ROLE_PORTAL_SUPERADMIN],
    ),
)
async def test_update_user(
    client,
    create_user_in_database,
    get_user_from_database,
    user_roles,
):
    user_data = {
        "user_id": uuid4(),
        "name": "dodir",
        "surname": "idodir",
        "email": "dodir@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": user_roles,
    }
    user_data_updated = {
        "name": "veter",
        "surname": "iveter",
        "email": "veter@example.com",
    }
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}",
        data=json.dumps(user_data_updated),
        headers=create_test_auth_headers_for_user(user_data["email"]),
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_updated["name"]
    assert user_from_db["surname"] == user_data_updated["surname"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data["is_active"]
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_update_user_check_one_is_updated(
    client,
    create_user_in_database,
    get_user_from_database,
):
    user_data_1 = {
        "user_id": uuid4(),
        "name": "dodir",
        "surname": "idodir",
        "email": "dodir@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    user_data_2 = {
        "user_id": uuid4(),
        "name": "veter",
        "surname": "iveter",
        "email": "veter@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    user_data_3 = {
        "user_id": uuid4(),
        "name": "bred",
        "surname": "pitt",
        "email": "bred@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    user_data_updated = {
        "name": "leo",
        "surname": "dicaprio",
        "email": "leo@example.com",
    }
    for user_data in [user_data_1, user_data_2, user_data_3]:
        await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data_1['user_id']}",
        data=json.dumps(user_data_updated),
        headers=create_test_auth_headers_for_user(user_data_1["email"]),
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data_1["user_id"])
    users_from_db = await get_user_from_database(user_data_1["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_updated["name"]
    assert user_from_db["surname"] == user_data_updated["surname"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data_1["is_active"]
    assert user_from_db["user_id"] == user_data_1["user_id"]

    users_from_db = await get_user_from_database(user_data_2["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_2["name"]
    assert user_from_db["surname"] == user_data_2["surname"]
    assert user_from_db["email"] == user_data_2["email"]
    assert user_from_db["is_active"] is user_data_2["is_active"]
    assert user_from_db["user_id"] == user_data_2["user_id"]

    users_from_db = await get_user_from_database(user_data_3["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_3["name"]
    assert user_from_db["surname"] == user_data_3["surname"]
    assert user_from_db["email"] == user_data_3["email"]
    assert user_from_db["is_active"] is user_data_3["is_active"]
    assert user_from_db["user_id"] == user_data_3["user_id"]


@pytest.mark.parametrize(
    "user_data_updated, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "name"],
                        "msg": "Field required",
                        "input": {},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "surname"],
                        "msg": "Field required",
                        "input": {},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "email"],
                        "msg": "Field required",
                        "input": {},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                ],
            },
        ),
        ({"name": "123"}, 422, {"detail": "Name should contains only letters"}),
        (
            {"email": ""},
            422,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "name"],
                        "msg": "Field required",
                        "input": {"email": ""},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "surname"],
                        "msg": "Field required",
                        "input": {"email": ""},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                    {
                        "type": "value_error",
                        "loc": ["body", "email"],
                        "msg": MSG,
                        "input": "",
                        "ctx": {
                            "reason": "The email address is not valid. It must have exactly one @-sign."
                        },
                    },
                ],
            },
        ),
        (
            {"surname": ""},
            422,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "name"],
                        "msg": "Field required",
                        "input": {"surname": ""},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                    {
                        "type": "string_too_short",
                        "loc": ["body", "surname"],
                        "msg": "String should have at least 1 characters",
                        "input": "",
                        "ctx": {"min_length": 1},
                        "url": "https://errors.pydantic.dev/2.4/v/string_too_short",
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "email"],
                        "msg": "Field required",
                        "input": {"surname": ""},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                ],
            },
        ),
        (
            {"name": ""},
            422,
            {
                "detail": [
                    {
                        "type": "string_too_short",
                        "loc": ["body", "name"],
                        "msg": "String should have at least 1 characters",
                        "input": "",
                        "ctx": {"min_length": 1},
                        "url": "https://errors.pydantic.dev/2.4/v/string_too_short",
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "surname"],
                        "msg": "Field required",
                        "input": {"name": ""},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "email"],
                        "msg": "Field required",
                        "input": {"name": ""},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                ],
            },
        ),
        ({"surname": "123"}, 422, {"detail": "Surname should contains only letters"}),
        (
            {"email": "123"},
            422,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "name"],
                        "msg": "Field required",
                        "input": {"email": "123"},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "surname"],
                        "msg": "Field required",
                        "input": {"email": "123"},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                    {
                        "type": "value_error",
                        "loc": ["body", "email"],
                        "msg": MSG,
                        "input": "123",
                        "ctx": {
                            "reason": "The email address is not valid. It must have exactly one @-sign."
                        },
                    },
                ],
            },
        ),
    ],
)
async def test_update_user_validation_error(
    client,
    create_user_in_database,
    get_user_from_database,
    user_data_updated,
    expected_status_code,
    expected_detail,
):
    user_data = {
        "user_id": uuid4(),
        "name": "dodir",
        "surname": "idodir",
        "email": "dodir@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}",
        data=json.dumps(user_data_updated),
        headers=create_test_auth_headers_for_user(user_data["email"]),
    )
    assert resp.status_code == expected_status_code
    resp_data = resp.json()
    assert resp_data == expected_detail


async def test_update_user_id_validation_error(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "dodir",
        "surname": "idodir",
        "email": "dodir@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    await create_user_in_database(**user_data)
    user_data_updated = {
        "name": "veter",
        "surname": "iveter",
        "email": "veter@example.com",
    }
    resp = client.patch(
        "/user/?user_id=123",
        data=json.dumps(user_data_updated),
        headers=create_test_auth_headers_for_user(user_data["email"]),
    )
    assert resp.status_code == 422
    data_from_response = resp.json()
    assert data_from_response == {
        "detail": [
            {
                "type": "uuid_parsing",
                "loc": ["query", "user_id"],
                "msg": "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 3",
                "input": "123",
                "ctx": {
                    "error": "invalid length: expected length 32 for simple format, found 3"
                },
                "url": "https://errors.pydantic.dev/2.4/v/uuid_parsing",
            },
        ],
    }


async def test_update_user_not_found_error(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "dodir",
        "surname": "idodir",
        "email": "dodir@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    await create_user_in_database(**user_data)
    user_data_updated = {
        "name": "bred",
        "surname": "pitt",
        "email": "bred@example.com",
    }
    user_id = uuid4()
    resp = client.patch(
        f"/user/?user_id={user_id}",
        data=json.dumps(user_data_updated),
        headers=create_test_auth_headers_for_user(user_data["email"]),
    )
    assert resp.status_code == 404
    resp_data = resp.json()
    assert resp_data == {"detail": f"User with id {user_id} not found."}


async def test_update_user_duplicate_email_error(client, create_user_in_database):
    user_data_1 = {
        "user_id": uuid4(),
        "name": "dodir",
        "surname": "idodir",
        "email": "dodir@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    user_data_2 = {
        "user_id": uuid4(),
        "name": "bred",
        "surname": "pitt",
        "email": "bred@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    user_data_updated = {
        "email": user_data_2["email"],
    }
    for user_data in [user_data_1, user_data_2]:
        await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data_1['user_id']}",
        data=json.dumps(user_data_updated),
        headers=create_test_auth_headers_for_user(user_data_1["email"]),
    )
    # assert resp.status_code == 503
    assert resp.status_code == 422
    assert resp.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "name"],
                "msg": "Field required",
                "input": {"email": "bred@example.com"},
                "url": "https://errors.pydantic.dev/2.4/v/missing",
            },
            {
                "type": "missing",
                "loc": ["body", "surname"],
                "msg": "Field required",
                "input": {"email": "bred@example.com"},
                "url": "https://errors.pydantic.dev/2.4/v/missing",
            },
        ],
    }
