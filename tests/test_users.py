from tests.tests_config import client
from utils.jwt_handler import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta


def test_user_without_subscription():
    create_operation = client.post("/user", json={
        "email": "test_without_subscription@example.com",
        "username": "test_without_subscription",
        "password": "test_without_subscription"
    })
    assert create_operation.status_code == 200, create_operation.text
    create_data = create_operation.json()
    assert create_data["email"] == "test_without_subscription@example.com"
    assert "id" in create_data
    user_id = create_data["id"]

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "test_without_subscription"}, expires_delta=access_token_expires
    )
    authorization_header = "Bearer " + access_token
    read_operation = client.get(f"/user/{user_id}", headers={"Authorization": authorization_header})
    assert read_operation.status_code == 200, read_operation.text
    read_data = read_operation.json()
    assert read_data["id"] == user_id
    assert read_data["email"] == "test_without_subscription@example.com"
    assert read_data["subscription_id"] == None

    update_operation = client.put(f"/user/{user_id}", json={
        "email": "test_without_subscription_updated@example.com",
        "username": "test_without_subscription_updated",
        "password": "test_without_subscription_updated"
    }, headers={"Authorization": authorization_header})
    assert update_operation.status_code == 200, update_operation.text
    update_data = update_operation.json()
    assert update_data["id"] == user_id
    assert update_data["email"] == "test_without_subscription_updated@example.com"
    assert update_data["subscription_id"] == None

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "test_without_subscription_updated"}, expires_delta=access_token_expires
    )
    authorization_header = "Bearer " + access_token
    delete_operation = client.delete(f"/user/{user_id}", headers={"Authorization": authorization_header})
    assert delete_operation.status_code == 200, delete_operation.text
    delete_data = delete_operation.json()
    assert delete_data["id"] == user_id


def test_create_user_with_subscription():
    create_operation = client.post("/user", json={
        "email": "test_with_subscription@example.com",
        "username": "test_with_subscription",
        "password": "test_with_subscription",
        "subscription_id": 1
    })
    assert create_operation.status_code == 200, create_operation.text
    create_data = create_operation.json()
    assert create_data["email"] == "test_with_subscription@example.com"
    assert "id" in create_data
    user_id = create_data["id"]

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "test_with_subscription"}, expires_delta=access_token_expires
    )
    authorization_header = "Bearer " + access_token
    read_operation = client.get(f"/user/{user_id}", headers={"Authorization": authorization_header})
    assert read_operation.status_code == 200, read_operation.text
    read_data = read_operation.json()
    assert read_data["id"] == user_id
    assert read_data["email"] == "test_with_subscription@example.com"
    assert read_data["subscription_id"] == 1

    update_operation = client.put(f"/user/{user_id}", json={
        "email": "test_with_subscription_updated@example.com",
        "username": "test_with_subscription_updated",
        "password": "test_with_subscription_updated",
        "subscription_id": 2
    }, headers={"Authorization": authorization_header})
    assert update_operation.status_code == 200, update_operation.text
    update_data = update_operation.json()
    assert update_data["id"] == user_id
    assert update_data["email"] == "test_with_subscription_updated@example.com"
    assert update_data["subscription_id"] == 2

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "test_with_subscription_updated"}, expires_delta=access_token_expires
    )
    authorization_header = "Bearer " + access_token
    delete_operation = client.delete(f"/user/{user_id}", headers={"Authorization": authorization_header})
    assert delete_operation.status_code == 200, delete_operation.text
    delete_data = delete_operation.json()
    assert delete_data["id"] == user_id


def test_read_users():
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "test_without_subscription"}, expires_delta=access_token_expires
    )
    authorization_header = "Bearer " + access_token
    response = client.get("/user", headers={"Authorization": authorization_header})
    assert response.status_code == 200