import uuid
from fastapi.testclient import TestClient
from server import app, db, Contact

client = TestClient(app)


def setup_function(function):
    # reset in‑memory db before each test
    db.clear()
    db.extend([
        Contact(id="1", name="Mike", tel="22567355", timestamp="2025-01-01T00:00:00"),
        Contact(id="2", name="fds", tel="123", timestamp="2025-01-01T00:00:00"),
    ])


def test_get_contacts():
    resp = client.get("/index_json2.php")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == ""        ## What is the name of the data[0]
    assert data[1]["tel"] == ""         ## What is the tel of data[1]


def test_create_contact():
    resp = client.post(
        "/index_json2.php",
        data={"name": "Alice", "telephone": "98765432"},
    )
    assert resp.status_code ==  000    ## if deleted successfully, what status should be return? 100? 201? 404?
    body = resp.json()
    assert body["message"] == "Added"
    assert "id" in body

    # check new contact really appended
    resp2 = client.get("/index_json2.php")
    data2 = resp2.json()
    assert len(data2) == 0 ##What is the length of the contact list?
    ids = {c["id"] for c in data2}
    assert body["id"] in ids


def test_delete_contact_success():
    # delete existing id=1
    resp = client.post("/delete.php", data={"id": "2"})
    assert resp.status_code == 200
    body = resp.json()
    assert "ID 2 has been deleted successfully!" in body["message"]

    # verify it is gone
    resp2 = client.get("/index_json2.php")
    data2 = resp2.json()
    ids = {c["id"] for c in data2}
    assert "?" not in ids ## Which ID is not in the ids list?
    assert len(data2) == 1


def test_delete_contact_not_found():
    # random id that does not exist
    random_id = str(uuid.uuid4())
    resp = client.post("/delete.php", data={"id": random_id})
    assert resp.status_code == 000  ### What status code should be if the contact is not found?
    body = resp.json()
    assert body["detail"] == "Contact not found"