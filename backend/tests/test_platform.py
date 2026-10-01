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


def test_driver_truck_assignment_and_unassignment():
    driver = client.post(
        "/drivers/",
        json={
            "name": "AUTOMATED TEST DRIVER",
            "phone": "555-0100",
            "company_name": "Automated Test Company",
        },
    )
    assert driver.status_code == 200
    driver_id = driver.json()["id"]

    truck = client.post(
        "/trucks/",
        json={
            "unit_number": "AUTO-TEST-TRUCK",
            "driver_id": driver_id,
        },
    )
    assert truck.status_code == 200
    truck_id = truck.json()["id"]
    assert truck.json()["driver_name"] == "AUTOMATED TEST DRIVER"
    assert truck.json()["driver_company_name"] == "Automated Test Company"

    driver_view = client.get(f"/drivers/{driver_id}")
    assert driver_view.status_code == 200
    assert driver_view.json()["truck_id"] == truck_id
    assert driver_view.json()["truck_unit_number"] == "AUTO-TEST-TRUCK"

    unassign = client.post(f"/trucks/{truck_id}/unassign-driver")
    assert unassign.status_code == 200
    assert unassign.json()["driver_id"] is None

    driver_view = client.get(f"/drivers/{driver_id}")
    assert driver_view.status_code == 200
    assert driver_view.json()["truck_id"] is None
    assert driver_view.json()["truck_unit_number"] is None

    client.delete(f"/trucks/{truck_id}")
    client.delete(f"/drivers/{driver_id}")


def test_delete_driver_preserves_truck():
    driver = client.post(
        "/drivers/",
        json={
            "name": "DELETE DRIVER TEST",
            "phone": "555-0101",
            "company_name": "Delete Driver Company",
        },
    )
    assert driver.status_code == 200
    driver_id = driver.json()["id"]

    truck = client.post(
        "/trucks/",
        json={
            "unit_number": "DELETE-DRIVER-TRUCK",
            "driver_id": driver_id,
        },
    )
    assert truck.status_code == 200
    truck_id = truck.json()["id"]

    deleted = client.delete(
        f"/drivers/{driver_id}",
        params={"delete_truck": False},
    )
    assert deleted.status_code == 200
    assert deleted.json()["truck_deleted"] is False

    truck_view = client.get(f"/trucks/{truck_id}")
    assert truck_view.status_code == 200
    assert truck_view.json()["driver_id"] is None

    client.delete(f"/trucks/{truck_id}")


def test_delete_truck_preserves_driver():
    driver = client.post(
        "/drivers/",
        json={
            "name": "DELETE TRUCK TEST",
            "phone": "555-0102",
            "company_name": "Delete Truck Company",
        },
    )
    assert driver.status_code == 200
    driver_id = driver.json()["id"]

    truck = client.post(
        "/trucks/",
        json={
            "unit_number": "DELETE-TRUCK-TEST",
            "driver_id": driver_id,
        },
    )
    assert truck.status_code == 200
    truck_id = truck.json()["id"]

    deleted = client.delete(
        f"/trucks/{truck_id}",
        params={"delete_driver": False},
    )
    assert deleted.status_code == 200
    assert deleted.json()["driver_deleted"] is False

    driver_view = client.get(f"/drivers/{driver_id}")
    assert driver_view.status_code == 200
    assert driver_view.json()["truck_id"] is None

    client.delete(f"/drivers/{driver_id}")


def test_combined_driver_and_truck_delete():
    driver = client.post(
        "/drivers/",
        json={
            "name": "COMBINED DELETE TEST",
            "phone": "555-0103",
            "company_name": "Combined Delete Company",
        },
    )
    assert driver.status_code == 200
    driver_id = driver.json()["id"]

    truck = client.post(
        "/trucks/",
        json={
            "unit_number": "COMBINED-DELETE-TEST",
            "driver_id": driver_id,
        },
    )
    assert truck.status_code == 200
    truck_id = truck.json()["id"]

    deleted = client.delete(
        f"/drivers/{driver_id}",
        params={"delete_truck": True},
    )
    assert deleted.status_code == 200
    assert deleted.json()["truck_deleted"] is True

    assert client.get(f"/drivers/{driver_id}").status_code == 404
    assert client.get(f"/trucks/{truck_id}").status_code == 404
