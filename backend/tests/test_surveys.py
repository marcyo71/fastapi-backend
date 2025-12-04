
from app import app, Depends
from app.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.db import Base, get_db
from backend.routers import user_router, survey_router
import backend.models.user
import backend.models.survey_model
import backend.models.user


# 🔧 Connessione persistente condivisa
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
connection = engine.connect()
TestingSessionLocal = sessionmaker(bind=connection)

# 🛠️ Crea le tabelle sulla connessione viva
Base.metadata.create_all(bind=connection)

# 🔁 Override della dipendenza
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🧪 App app isolata
app = app()
app.include_router(user_router.router)
app.include_router(survey_router.router)
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_user_and_survey():
    user = {"name": "Marcello", "email": "marcy@example.com"}
    res_user = client.post("/users/", json=user)
    assert res_user.status_code == 200
    user_id = res_user.json()["id"]

    survey = {
        "title": "Test Survey",
        "reward": 5.0,
        "provider": "SurveyMaster",
        "user_id": user_id
    }
    res_survey = client.post("/surveys/", json=survey)
    assert res_survey.status_code == 200
    assert res_survey.json()["title"] == "Test Survey"
def test_get_user_surveys(client):
    # Crea utente
    user = {"name": "Marcello", "email": "marcy@example.com"}
    res_user = client.post("/users/", json=user)
    assert res_user.status_code == 200
    user_id = res_user.json()["id"]

    # Crea due sondaggi per quell’utente
    surveys = [
        {"title": "Sondaggio A", "reward": 3.5, "provider": "ProviderX", "user_id": user_id},
        {"title": "Sondaggio B", "reward": 2.0, "provider": "ProviderY", "user_id": user_id}
    ]
    for s in surveys:
        res = client.post("/surveys/", json=s)
        assert res.status_code == 200

    # Recupera i sondaggi dell’utente
    res_surveys = client.get(f"/users/{user_id}/surveys")
    assert res_surveys.status_code == 200
    data = res_surveys.json()

    assert isinstance(data, list)
    assert len(data) == 2
    titles = [s["title"] for s in data]
    assert "Sondaggio A" in titles
    assert "Sondaggio B" in titles
import pytest

@pytest.mark.parametrize("user_data,surveys,expected_titles", [
    (
        {"name": "Alice", "email": "alice@example.com"},
        [
            {"title": "Survey A1", "reward": 2.0, "provider": "X"},
            {"title": "Survey A2", "reward": 3.0, "provider": "Y"}
        ],
        ["Survey A1", "Survey A2"]
    ),
    (
        {"name": "Bob", "email": "bob@example.com"},
        [
            {"title": "Survey B1", "reward": 1.5, "provider": "Z"}
        ],
        ["Survey B1"]
    ),
    (
        {"name": "Charlie", "email": "charlie@example.com"},
        [],
        []
    )
])
def test_get_user_surveys_parametrized(client, user_data, surveys, expected_titles):
    # Crea utente
    res_user = client.post("/users/", json=user_data)
    assert res_user.status_code == 200
    user_id = res_user.json()["id"]

    # Crea sondaggi
    for s in surveys:
        s["user_id"] = user_id
        res = client.post("/surveys/", json=s)
        assert res.status_code == 200

    # Recupera sondaggi
    res_surveys = client.get(f"/users/{user_id}/surveys")
    assert res_surveys.status_code == 200
    data = res_surveys.json()

    assert isinstance(data, list)
    assert len(data) == len(expected_titles)
    titles = [s["title"] for s in data]
    for title in expected_titles:
        assert title in titles

def test_delete_nonexistent_survey():
    response = client.delete("/surveys/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Survey not found"
def test_create_user_duplicate_email():
    user_data = {"email": "test@example.com", "name": "Marcello"}
    response1 = client.post("/users/", json=user_data)
    assert response1.status_code == 201

    response2 = client.post("/users/", json=user_data)
    assert response2.status_code in [409, 422]  # dipende da come gestisci il vincolo


