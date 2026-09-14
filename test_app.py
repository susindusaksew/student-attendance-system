import pytest
from app import app, init_db


@pytest.fixture
def client(tmp_path, monkeypatch):

    test_database = tmp_path / "test_attendance.db"

    monkeypatch.setattr(
        "app.DATABASE",
        str(test_database)
    )

    init_db()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200


def test_add_student(client):

    response = client.post(
        "/add",
        data={
            "student_id": "TEST001",
            "name": "Test Student"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Test Student" in response.data
    assert b"TEST001" in response.data


def test_mark_present(client):

    client.post(
        "/add",
        data={
            "student_id": "TEST002",
            "name": "Another Student"
        }
    )

    response = client.get(
        "/attendance/1/Present",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Present" in response.data


def test_delete_student(client):

    client.post(
        "/add",
        data={
            "student_id": "TEST003",
            "name": "Delete Student"
        }
    )

    response = client.get(
        "/delete/1",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Delete Student" not in response.data