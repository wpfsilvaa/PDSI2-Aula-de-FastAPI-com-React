from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_hello():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"Hello": "World!"}


def test_quadrado():
    num = 4
    response = client.get(f'/quadrado/{num}')
    assert response.status_code == 200
    assert response.text == str(num ** 2)
