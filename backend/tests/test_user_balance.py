import uuid
import pytest

# ✅ Test base: creazione utente e sondaggi, verifica balance
def test_user_balance_with_surveys(client):
    unique_email = f"marcy_{uuid.uuid4().hex}@example.com"
    user = {"name": "Marcello", "email": unique_email}
    res_user = client.post("/users/", json=user)
    assert res_user.status_code == 200
    user_id = res_user.json()["id"]

    surveys = [
        {"title": "Sondaggio A", "reward": 3.5, "provider": "ProviderX", "user_id": user_id},
        {"title": "Sondaggio B", "reward": 2.0, "provider": "ProviderY", "user_id": user_id},
        {"title": "Sondaggio C", "reward": 4.5, "provider": "ProviderZ", "user_id": user_id}
    ]
    for s in surveys:
        res = client.post("/surveys/", json=s)
        assert res.status_code == 200

    res_balance = client.get(f"/users/{user_id}/balance")
    assert res_balance.status_code == 200
    assert res_balance.json()["balance"] == 10.0

# ✅ Test parametrico: edge cases sul reward
@pytest.mark.parametrize("surveys,expected_balance", [
    ([("A", 1.0), ("B", 2.0)], 3.0),
    ([("A", 0.1), ("B", 0.2)], pytest.approx(0.3)),
])
def test_user_balance_edge_cases(client, create_user, create_survey, surveys, expected_balance):
    user_id = create_user("EdgeCaseUser")
    for title, reward in surveys:
        create_survey(title, reward, "ProviderX", user_id)

    res = client.get(f"/users/{user_id}/balance")
    assert res.status_code == 200
    assert res.json()["balance"] == expected_balance

# ✅ Test: reward negativo → deve fallire
def test_create_survey_with_negative_reward(client, create_user):
    user_id = create_user("Marcello")
    payload = {
        "title": "Sondaggio Negativo",
        "reward": -5.0,
        "provider": "ProviderX",
        "user_id": user_id
    }
    res = client.post("/surveys/", json=payload)
    assert res.status_code == 422

# ✅ Test: reward non valido (None, stringa)
@pytest.mark.parametrize("reward", [None, "not_a_number"])
def test_create_survey_with_invalid_reward(client, create_user, reward):
    user_id = create_user("Marcello")
    payload = {
        "title": "Sondaggio Invalid",
        "reward": reward,
        "provider": "ProviderX",
        "user_id": user_id
    }
    res = client.post("/surveys/", json=payload)
    assert res.status_code in [400, 422]

# ✅ Test: eliminazione sondaggio e aggiornamento balance
def test_delete_survey_and_update_balance(client, create_user, create_survey):
    user_id = create_user("Marcello")
    survey_payloads = [
        {"title": "A", "reward": 5.0, "provider": "X", "user_id": user_id},
        {"title": "B", "reward": 3.0, "provider": "Y", "user_id": user_id}
    ]
    survey_ids = []
    for payload in survey_payloads:
        res = client.post("/surveys/", json=payload)
        assert res.status_code == 200
        survey_ids.append(res.json()["id"])

    res_balance = client.get(f"/users/{user_id}/balance")
    assert res_balance.status_code == 200
    assert res_balance.json()["balance"] == 8.0

    res_delete = client.delete(f"/surveys/{survey_ids[0]}")
    assert res_delete.status_code == 204

    res_balance = client.get(f"/users/{user_id}/balance")
    assert res_balance.status_code == 200
    assert res_balance.json()["balance"] == 3.0
