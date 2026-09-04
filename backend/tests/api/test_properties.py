import pytest

def test_create_property(client):
    response = client.post(
        "/api/v1/properties/",
        json={
            "name": "Test Property",
            "address": "123 Test St",
            "city": "Testville",
            "state": "TS",
            "zip_code": "12345",
            "property_type": "Apartment",
            "year_built": 2020
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Property"
    assert "id" in data

def test_read_properties(client, db_session):
    # First create one
    client.post(
        "/api/v1/properties/",
        json={
            "name": "Test Property 2",
            "address": "456 Test Ave",
            "city": "Testville",
            "state": "TS",
            "zip_code": "12345",
            "property_type": "House",
        },
    )
    
    response = client.get("/api/v1/properties/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Test Property 2"

def test_update_property(client):
    create_response = client.post(
        "/api/v1/properties/",
        json={
            "name": "Old Name",
            "address": "123 Test St",
            "city": "Testville",
            "state": "TS",
            "zip_code": "12345",
            "property_type": "Apartment",
        },
    )
    prop_id = create_response.json()["id"]
    
    update_response = client.patch(
        f"/api/v1/properties/{prop_id}",
        json={"name": "New Name"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "New Name"

def test_delete_property(client):
    create_response = client.post(
        "/api/v1/properties/",
        json={
            "name": "Delete Me",
            "address": "123 Test St",
            "city": "Testville",
            "state": "TS",
            "zip_code": "12345",
            "property_type": "Apartment",
        },
    )
    prop_id = create_response.json()["id"]
    
    delete_response = client.delete(f"/api/v1/properties/{prop_id}")
    assert delete_response.status_code == 204
    
    get_response = client.get(f"/api/v1/properties/{prop_id}")
    assert get_response.status_code == 404
