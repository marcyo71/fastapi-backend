def test_user_payout_eligibility(client):
    user_data = {"email": "payout@example.com", "name": "PayoutUser"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]

    # saldo iniziale = 0.0 → non idoneo
    response = client.get(f"/users/{user_id}/payout")
    assert response.status_code == 200
    assert response.json()["eligible"] is False

def test_user_withdraw_insufficient_balance(client):
    user_data = {"email": "withdraw@example.com", "name": "WithdrawUser"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]

    response = client.post(f"/users/{user_id}/withdraw")
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance for payout"

def test_user_payout_eligible(client):
    user_data = {"email": "rich@example.com", "name": "RichUser"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]

    # Simula saldo manuale
    client.put(f"/users/{user_id}/balance", json={"balance": 15.0})  # endpoint da creare se non esiste

    response = client.get(f"/users/{user_id}/payout")
    assert response.status_code == 200
    assert response.json()["eligible"] is True
def test_user_payout_eligible(client):
    user_data = {"email": "rich@example.com", "name": "RichUser"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]

    # Simula saldo manuale
    client.put(f"/users/{user_id}/balance", json={"balance": 15.0})  # endpoint da creare se non esiste

    response = client.get(f"/users/{user_id}/payout")
    assert response.status_code == 200
    assert response.json()["eligible"] is True

def test_user_withdraw_success(client, create_user, create_balance):
    user_id = create_user("CashOut")
    balance = create_balance(user_id, 20.0)

    res = client.post(f"/users/{user_id}/withdraw")
    assert res.status_code == 200
    assert res.json()["new_balance"] == 0.0

def test_user_payout_eligible(client, create_user, create_balance):
    user_id = create_user("RichUser")
    balance = create_balance(user_id, 15.0)

    res = client.get(f"/users/{user_id}/payout")
    assert res.status_code == 200
    assert res.json()["eligible"] is True
    assert res.json()["balance"] == 15.0



