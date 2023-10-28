# from tests.conftest import client
#
#
# async def test_create_user(get_user_from_database):
#     user_data = {
#         "name": "dodir",
#         "surname": "idodir",
#         "email": "dodir@example.com",
#     }
#     response = client.post(
#         "/user/",
#         json=user_data,
#     )
#     assert response.status_code == 200
#     data_from_response = response.json()
#     assert data_from_response["name"] == user_data["name"]
#     assert data_from_response["surname"] == user_data["surname"]
#     assert data_from_response["email"] == user_data["email"]
#     assert data_from_response["is_active"] is True
#     users_from_db = await get_user_from_database(data_from_response["user_id"])
#     assert len(users_from_db) == 1
#     user_from_db = dict(users_from_db[0])
#     assert user_from_db["name"] == user_data["name"]
#     assert user_from_db["surname"] == user_data["surname"]
#     assert user_from_db["email"] == user_data["email"]
#     assert user_from_db["is_active"] is True
#     assert str(user_from_db["user_id"]) == data_from_response["user_id"]
