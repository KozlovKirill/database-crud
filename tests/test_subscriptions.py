from tests.tests_config import client

def test_create_subscription():
    request = client.post("/subscription", json={
        "name": "test",
        "description": "test",
        "price": 1,
        "period": 1,
        "previlegis": ["test"]
    })
    assert request.status_code == 200

def test_create_subscription_without_description():
    request = client.post("/subscription", json={
        "name": "no_description_test",
        "price": 1,
        "period": 1,
        "previlegis": ["no_description_test"]
    })
    assert request.status_code == 200

def test_create_subscription_without_price():
    request = client.post("/subscription", json={
        "name": "no_price_test",
        "description": "no_price_test",
        "period": 1,
        "previlegis": ["no_price_test"]
    })
    assert request.status_code == 200

def test_create_subscription_without_price_and_description():
    request = client.post("/subscription", json={
        "name": "no_price_and_description_test",
        "period": 1,
        "previlegis": ["no_price_and_description_test"]
    })
    assert request.status_code == 200

def test_read_all_subscription():
    response = client.get("/subscription")
    assert response.status_code == 200