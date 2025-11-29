def test_get_users_accessible(client):
    response = client.get("/users/")
    assert response.status_code == 200

def test_get_users_accessible(client):
    response = client.get("/surveys/")
    assert response.status_code == 200
