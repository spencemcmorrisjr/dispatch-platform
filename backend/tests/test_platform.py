from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Dispatch OS API running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_driver_endpoint_exists():
    response = client.get("/drivers/")
    assert response.status_code == 200


def test_truck_endpoint_exists():
    response = client.get("/trucks/")
    assert response.status_code == 200


def test_load_endpoint_exists():
    response = client.get("/loads/")
    assert response.status_code == 200


def test_expense_endpoint_exists():
    response = client.get("/expenses/")
    assert response.status_code == 200
