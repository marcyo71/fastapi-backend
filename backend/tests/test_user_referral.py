def test_user_referral_reward(client, unique_email):
    # Crea referrer
    referrer_email = unique_email("referrer")
    res1 = client.post("/users/", json={"name": "Referrer", "email": referrer_email})
    ref_code = res1.json()["ref_code"]

    # Crea referenziato
    referred_email = unique_email("referred")
    res2 = client.post("/users/", json={"name": "Referred", "email": referred_email, "ref_by": ref_code})
    assert res2.status_code == 200

    # Verifica reward al referrer
    referrer_id = res1.json()["id"]
    res_balance = client.get(f"/users/{referrer_id}/balance")
    assert res_balance.status_code == 200
    assert res_balance.json()["balance"] == 1.0

def test_user_referral_dashboard(client, unique_email):
    # Crea referrer
    referrer_email = unique_email("referrer")
    res1 = client.post("/users/", json={"name": "Referrer", "email": referrer_email})
    ref_code = res1.json()["ref_code"]
    referrer_id = res1.json()["id"]

    # Crea 3 utenti referenziati
    for i in range(3):
        email = unique_email(f"referred{i}")
        res = client.post("/users/", json={"name": f"Referred{i}", "email": email, "ref_by": ref_code})
        assert res.status_code == 200

    # Verifica dashboard referral
    res_dash = client.get(f"/users/{referrer_id}/referrals")
    assert res_dash.status_code == 200
    data = res_dash.json()
    assert data["count"] == 3
    assert data["ref_code"] == ref_code
    assert all("email" in r and "name" in r for r in data["referrals"])
def test_referral_reward_cumulative(client, unique_email):
    # Crea referrer
    referrer_email = unique_email("referrer")
    res1 = client.post("/users/", json={"name": "Referrer", "email": referrer_email})
    ref_code = res1.json()["ref_code"]
    referrer_id = res1.json()["id"]

    # Crea referenziato
    referred_email = unique_email("referred")
    res2 = client.post("/users/", json={"name": "Referred", "email": referred_email, "ref_by": ref_code})
    referred_id = res2.json()["id"]

    # Crea sondaggi per il referenziato
    surveys = [
        {"title": "S1", "reward": 10.0, "provider": "P1", "user_id": referred_id},
        {"title": "S2", "reward": 5.0, "provider": "P2", "user_id": referred_id}
    ]
    for s in surveys:
        res = client.post("/surveys/", json=s)
        assert res.status_code == 200

    # Verifica bilancio referrer: 1.0 (bonus) + 10% di 15.0 = 2.5
    res_balance = client.get(f"/users/{referrer_id}/balance")
    assert res_balance.status_code == 200
    assert res_balance.json()["balance"] == 2.5

def test_invalid_ref_by(client, unique_email):
    email = unique_email("badref")
    res = client.post("/users/", json={"name": "BadRef", "email": email, "ref_by": "nonexistent"})
    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid referral code"

def test_circular_referral(client, unique_email):
    email = unique_email("selfref")
    res = client.post("/users/", json={"name": "SelfRef", "email": email})
    ref_code = res.json()["ref_code"]

    res2 = client.post("/users/", json={"name": "Loop", "email": unique_email("loop"), "ref_by": ref_code})
    assert res2.status_code == 200

    # Tentativo di referenziare se stesso
    res3 = client.post("/users/", json={"name": "Circular", "email": unique_email("circular"), "ref_by": res3.json()["ref_code"]})
    assert res3.status_code == 400
    assert res3.json()["detail"] == "Circular referral not allowed"


