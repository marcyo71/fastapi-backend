import httpx

BASE_URL = "http://127.0.0.1:8000"

def test_login(username, password):
    with httpx.Client(base_url=BASE_URL, follow_redirects=True) as client:
        # Simula POST /login
        response = client.post("/login", data={"username": username, "password": password})
        print("Login status:", response.status_code)
        print("Set-Cookie header:", response.headers.get("set-cookie"))

        # Ora chiama /whoami con il cookie
        whoami = client.get("/whoami")
        print("Whoami status:", whoami.status_code)
        print("Whoami JSON:", whoami.json())

if __name__ == "__main__":
    print("---- Test admin ----")
    test_login("admin", "segreto")

    print("\n---- Test marcy ----")
    test_login("marcy", "123")
