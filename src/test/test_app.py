from ..backend.app import *
import json
import pytest
from typing import Set
from flask.testing import FlaskClient


@pytest.fixture
def client() -> FlaskClient:
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_schema_from_file():
    schema = get_schema_from_file()
    assert schema is not None

    schema_dict = json.loads(schema)
    assert "description" in schema_dict
    assert schema_dict["description"] != ""

    assert "regex" in schema_dict
    assert schema_dict["regex"] != ""


def test_get_schema_regex():
    regex = get_schema_regex()
    assert regex is not None
    assert regex != ""


def test_get_schema_service(client):
    rv = client.get("/schema")
    assert rv is not None
    assert rv.status_code == 200

    schema = rv.get_json()
    assert schema is not None
    assert "description" in schema
    assert schema["description"] != ""
    assert "regex" in schema
    assert schema["regex"] != ""


def test_happy_path_domain_operations(client):
    # Add domain
    name: str = "canberra"
    rv = client.post("/domains", json={"name": name})
    assert rv is not None
    assert rv.status_code == 201

    domain = rv.get_json()
    assert domain is not None
    assert "id" in domain
    assert domain["id"] > 0
    assert "name" in domain
    assert domain["name"] == name
    assert "platforms" in domain
    assert len(domain["platforms"]) == 0

    domain_id: int = int(domain["id"])

    # Get domain
    rv = client.get(f"/domains/{domain_id}")
    assert rv is not None
    assert rv.status_code == 200

    domain = rv.get_json()
    assert domain is not None
    assert "id" in domain
    assert domain["id"] == domain_id
    assert "name" in domain
    assert domain["name"] == name
    assert "platforms" in domain
    assert len(domain["platforms"]) == 0

    # Update domain
    new_name: str = "hobart"
    rv = client.put(
        "/domains",
        json={
            "id": domain_id,
            "name": new_name,
        },
    )
    assert rv is not None
    assert rv.status_code == 202

    domain = rv.get_json()
    assert domain is not None
    assert "id" in domain
    assert domain["id"] == domain_id
    assert "name" in domain
    assert domain["name"] == new_name
    assert "platforms" in domain
    assert len(domain["platforms"]) == 0

    # Get all domains
    rv = client.get("/domains")
    assert rv is not None
    assert rv.status_code == 200

    domains = rv.get_json()
    assert domains is not None
    assert len(domains) > 0

    for domain in domains:
        assert "id" in domain
        assert "name" in domain
        assert "platforms" in domain

    # Delete domain
    rv = client.delete(f"/domains/{domain_id}")
    assert rv is not None
    assert rv.status_code == 202

    response = rv.get_json()
    assert response is not None
    assert "success" in response
    assert response["success"] == True
    assert "message" in response
    assert response["message"] == f"Deleted domain with ID {domain_id}"


def test_unhappy_path_domain_operations(client):
    # Get domain that doesn't exist - none will ever have ID 0 in sqlite
    rv = client.get(f"/domains/0")
    assert rv is not None
    assert rv.status_code == 204

    # Update domain that doesn't exist
    rv = client.put(
        "/domains",
        json={
            "id": 0,
            "name": "hobart",
        },
    )
    assert rv is not None
    assert rv.status_code == 500

    response = rv.get_json()
    assert response is not None
    assert "success" in response
    assert response["success"] == False
    assert "message" in response
    assert response["message"] == f"Could not find domain with ID 0"

    # Delete domain that doesn't exist
    rv = client.delete(f"/domains/0")
    assert rv is not None
    assert rv.status_code == 500

    response = rv.get_json()
    assert response is not None
    assert "success" in response
    assert response["success"] == False
    assert "message" in response
    assert response["message"] == f"Could not find domain with ID 0"


def test_happy_path_platform_operations(client):
    # Add domain for platform operations
    rv = client.post("/domains", json={"name": "canberra"})
    assert rv is not None
    assert rv.status_code == 201

    domain = rv.get_json()
    assert domain is not None
    domain_id = int(domain["id"])

    # Get available platforms for new domain
    rv = client.get(f"/domains/available_platforms/{domain_id}")
    assert rv is not None
    assert rv.status_code == 200

    available = rv.get_json()
    assert available is not None
    assert "available" in available
    assert len(available["available"]) == 5
    expected_available: Set[int] = {1, 2, 3, 4, 5}
    actual_available: Set[int] = set(available["available"])
    assert expected_available == actual_available

    # Add platform
    nbr: int = 2
    txt: str = "[test] 1234"
    is_valid: bool = True
    rv = client.post(
        "/platforms",
        json={
            "domain_id": domain_id,
            "nbr": nbr,
            "txt": txt,
            "is_valid": is_valid,
        },
    )
    assert rv is not None
    assert rv.status_code == 201

    platform = rv.get_json()
    assert platform is not None
    assert "id" in platform
    assert platform["id"] > 0
    assert "domain_id" in platform
    assert platform["domain_id"] == domain_id
    assert "nbr" in platform
    assert platform["nbr"] == nbr
    assert "txt" in platform
    assert platform["txt"] == txt
    assert "is_valid" in platform
    assert platform["is_valid"] == is_valid

    platform_id: int = int(platform["id"])

    # Get platform
    rv = client.get(f"/platforms/{platform_id}")
    assert rv is not None
    assert rv.status_code == 200

    platform = rv.get_json()
    assert platform is not None
    assert "id" in platform
    assert platform["id"] == platform_id
    assert "domain_id" in platform
    assert platform["domain_id"] == domain_id
    assert "nbr" in platform
    assert platform["nbr"] == nbr
    assert "txt" in platform
    assert platform["txt"] == txt
    assert "is_valid" in platform
    assert platform["is_valid"] == is_valid

    # Update platform
    new_nbr: int = 3
    new_txt: str = "[tset] 4321"
    new_is_valid: bool = False
    rv = client.put(
        "/platforms",
        json={
            "id": platform_id,
            "domain_id": domain_id,
            "nbr": new_nbr,
            "txt": new_txt,
            "is_valid": new_is_valid,
        },
    )
    assert rv is not None
    assert rv.status_code == 202

    platform = rv.get_json()
    assert platform is not None
    assert "id" in platform
    assert platform["id"] == platform_id
    assert "domain_id" in platform
    assert platform["domain_id"] == domain_id
    assert "nbr" in platform
    assert platform["nbr"] == new_nbr
    assert "txt" in platform
    assert platform["txt"] == new_txt
    assert "is_valid" in platform
    assert platform["is_valid"] == new_is_valid

    # Get available platforms with platform added
    rv = client.get(f"/domains/available_platforms/{domain_id}")
    assert rv is not None
    assert rv.status_code == 200

    available = rv.get_json()
    assert available is not None
    assert "available" in available
    assert len(available["available"]) == 4
    expected_available: Set[int] = {1, 2, 4, 5}
    actual_available: Set[int] = set(available["available"])
    assert expected_available == actual_available

    # Delete platform
    rv = client.delete(f"/platforms/{platform_id}")
    assert rv is not None
    assert rv.status_code == 202

    response = rv.get_json()
    assert response is not None
    assert "success" in response
    assert response["success"] == True
    assert "message" in response
    assert response["message"] == f"Deleted platform with ID {platform_id}"

    # Delete domain
    rv = client.delete(f"/domains/{domain_id}")
    assert rv is not None
    assert rv.status_code == 202

    response = rv.get_json()
    assert response is not None


def test_unhappy_path_platform_operations(client):
    # Get platform that doesn't exist
    rv = client.get("/platforms/0")
    assert rv is not None
    assert rv.status_code == 204

    # Update platform that doesn't exist
    rv = client.put(
        "/platforms",
        json={
            "id": 0,
            "domain_id": 1,
            "nbr": 1,
            "txt": "[test] 1234",
            "is_valid": False,
        },
    )
    assert rv is not None
    assert rv.status_code == 500

    response = rv.get_json()
    assert response is not None
    assert "success" in response
    assert response["success"] == False
    assert "message" in response
    assert response["message"] == f"Could not find platform with ID 0"

    # Delete platform that doesn't exist
    rv = client.delete("/platforms/0")
    assert rv is not None
    assert rv.status_code == 500

    response = rv.get_json()
    assert response is not None
    assert "success" in response
    assert response["success"] == False
    assert "message" in response
    assert response["message"] == f"Could not find platform with ID 0"
