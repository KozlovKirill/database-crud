from tests.tests_config import client

def test_read_main():
    responce = client.get("/")
    assert responce.status_code == 200
    assert responce.json() == {"Broadcast application": "v0.0.1"}