def test_checkout_success(client, create_user, create_balance):
    user_id = create_user("Pagante")
    create_balance(user_id, 12.5)

    res = client.post(f"/users/{user_id}/checkout")
    assert res.status_code == 200
    assert res.json()["status"] == "paid"
    assert res.json()["amount"] == 12.5

    res_check = client.get(f"/users/{user_id}/balance")
    assert res_check.json()["balance"] == 0.0


def test_checkout_insufficient_balance(client, create_user, create_balance):
    user_id = create_user("Povero")
    create_balance(user_id, 2.0)

    res = client.post(f"/users/{user_id}/checkout")
    assert res.status_code == 400
    assert res.json()["detail"] == "Insufficient balance for payout"
