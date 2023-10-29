import json

import pytest


async def test_create_user(client, get_user_from_database):
    user_data = {
        "name": "dodir",
        "surname": "idodir",
        "email": "dodir@example.com",
        "password": "SamplePass1!",
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]


async def test_create_user_duplicate_email_error(client, get_user_from_database):
    user_data = {
        "name": "dodir",
        "surname": "idodir",
        "email": "dodir@example.com",
        "password": "SamplePass1!",
    }
    user_data_same_email = {
        "name": "veter",
        "surname": "iveter",
        "email": "dodir@example.com",
        "password": "SamplePass1!",
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]
    resp = client.post("/user/", data=json.dumps(user_data_same_email))
    assert resp.status_code == 503
    assert (
        'duplicate key value violates unique constraint "users_email_key"'
        in resp.json()["detail"]
    )


MSG = "value is not a valid email address: The email address is not valid. It must have exactly one @-sign."


@pytest.mark.parametrize(
    "user_data_for_creation, expected_status_code, expected_detail",
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
                    {
                        "type": "missing",
                        "loc": ["body", "password"],
                        "msg": "Field required",
                        "input": {},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                ]
            },
        ),
        (
            {"name": 123, "surname": 456, "email": "lol"},
            422,
            {
                "detail": [
                    {
                        "type": "string_type",
                        "loc": ["body", "name"],
                        "msg": "Input should be a valid string",
                        "input": 123,
                        "url": "https://errors.pydantic.dev/2.4/v/string_type",
                    },
                    {
                        "type": "string_type",
                        "loc": ["body", "surname"],
                        "msg": "Input should be a valid string",
                        "input": 456,
                        "url": "https://errors.pydantic.dev/2.4/v/string_type",
                    },
                    {
                        "type": "value_error",
                        "loc": ["body", "email"],
                        "msg": MSG,
                        "input": "lol",
                        "ctx": {
                            "reason": "The email address is not valid. It must have exactly one @-sign."
                        },
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "password"],
                        "msg": "Field required",
                        "input": {"name": 123, "surname": 456, "email": "lol"},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                ]
            },
        ),
        (
            {"name": "dodir", "surname": 456, "email": "lol"},
            422,
            {
                "detail": [
                    {
                        "type": "string_type",
                        "loc": ["body", "surname"],
                        "msg": "Input should be a valid string",
                        "input": 456,
                        "url": "https://errors.pydantic.dev/2.4/v/string_type",
                    },
                    {
                        "type": "value_error",
                        "loc": ["body", "email"],
                        "msg": MSG,
                        "input": "lol",
                        "ctx": {
                            "reason": "The email address is not valid. It must have exactly one @-sign."
                        },
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "password"],
                        "msg": "Field required",
                        "input": {"name": "dodir", "surname": 456, "email": "lol"},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                ]
            },
        ),
        (
            {"name": "dodir", "surname": "idodir", "email": "dodir"},
            422,
            {
                "detail": [
                    {
                        "type": "value_error",
                        "loc": ["body", "email"],
                        "msg": MSG,
                        "input": "dodir",
                        "ctx": {
                            "reason": "The email address is not valid. It must have exactly one @-sign."
                        },
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "password"],
                        "msg": "Field required",
                        "input": {
                            "name": "dodir",
                            "surname": "idodir",
                            "email": "dodir",
                        },
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                ]
            },
        ),
    ],
)
async def test_create_user_validation_error(
    client, user_data_for_creation, expected_status_code, expected_detail
):
    resp = client.post("/user/", data=json.dumps(user_data_for_creation))
    data_from_resp = resp.json()
    assert resp.status_code == expected_status_code

    print()
    print("====================================")
    print()
    print(data_from_resp)
    print()
    print("=================================================")
    print()

    assert data_from_resp == expected_detail
