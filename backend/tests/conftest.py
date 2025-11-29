import pytest
import uuid
from fastapi.testclient import TestClient
from fastapi import FastAPI
from backend.db.init import init_db
from backend.db import Base, engine, get_db
from backend.routers import user_router, survey_router
from backend.tests.test_setup import TestingSessionLocal, connection  # forza la creazione delle tabelle

# ✅ Fixture client con override DB e ricreazione tabelle
@pytest.fixture(scope="function")
def client():
    # Ricrea le tabelle per isolamento
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = FastAPI()
    app.include_router(user_router.router)
    app.include_router(survey_router.router)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

# ✅ Generatore email uniche
@pytest.fixture
def unique_email():
    def _generate(base: str = "user") -> str:
        return f"{base}_{uuid.uuid4().hex}@example.com"
    return _generate

# ✅ Crea utente
@pytest.fixture
def create_user(client, unique_email):
    def _create(name="TestUser"):
        email = unique_email(name.lower())
        res = client.post("/users/", json={"name": name, "email": email})
        assert res.status_code == 200
        return res.json()["id"]
    return _create

# ✅ Crea sondaggio
@pytest.fixture
def create_survey(client):
    def _create(title, reward, provider, user_id):
        payload = {"title": title, "reward": reward, "provider": provider, "user_id": user_id}
        res = client.post("/surveys/", json=payload)
        assert res.status_code == 200
    return _create

# ✅ Imposta saldo utente
@pytest.fixture
def create_balance(client):
    def _set(user_id: int, amount: float):
        res = client.put(f"/users/{user_id}/balance", json={"balance": amount})
        assert res.status_code == 200
        return res.json()["balance"]
    return _set

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_db()
