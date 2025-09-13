from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_move_to_success():
    response = client.post("/execute_command", json={
        "command": "move_to",
        "x": 5,
        "y": 7,
        "message": "Going to (5,7)"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_move_to_missing_y():
    response = client.post("/execute_command", json={
        "command": "move_to",
        "x": 5,
        "message": "Missing y"
    })
    assert response.status_code == 422  # schema rejects invalid input

def test_move_to_invalid_type():
    response = client.post("/execute_command", json={
        "command": "move_to",
        "x": "five",   #  wrong type
        "y": 7,
        "message": "Invalid type"
    })
    assert response.status_code == 422


def test_rotate_success():
    response = client.post("/execute_command", json={
        "command": "rotate",
        "angle": 90,
        "direction": "clockwise",
        "message": "Rotate 90 clockwise"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_rotate_invalid_direction():
    response = client.post("/execute_command", json={
        "command": "rotate",
        "angle": 90,
        "direction": "left",  # invalid value
        "message": "Invalid direction"
    })
    assert response.status_code == 422

def test_rotate_missing_angle():
    response = client.post("/execute_command", json={
        "command": "rotate",
        "direction": "clockwise",
        "message": "Missing angle"
    })
    assert response.status_code == 422


def test_start_patrol_success():
    response = client.post("/execute_command", json={
        "command": "start_patrol",
        "route_id": "first_floor",
        "speed": "fast",
        "repeat_count": 3,
        "message": "Patrolling"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_start_patrol_invalid_route():
    response = client.post("/execute_command", json={
        "command": "start_patrol",
        "route_id": "roof",  # not allowed
        "message": "Invalid route"
    })
    assert response.status_code == 422

def test_start_patrol_default_speed():
    response = client.post("/execute_command", json={
        "command": "start_patrol",
        "route_id": "bedrooms",
        "message": "No speed provided"
    })
    data = response.json()
    assert response.status_code == 200
    # speed defaults to medium
    assert data["command"]["speed"] == "medium"

def test_start_patrol_repeat_count_infinite():
    response = client.post("/execute_command", json={
        "command": "start_patrol",
        "route_id": "second_floor",
        "repeat_count": -1,  # allowed infinite loop
        "message": "Infinite patrol"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_start_patrol_repeat_count_invalid():
    response = client.post("/execute_command", json={
        "command": "start_patrol",
        "route_id": "first_floor",
        "repeat_count": 0,  # ❌ not allowed (must be ≥ 1 or -1)
        "message": "Invalid repeat count"
    })
    assert response.status_code == 422
