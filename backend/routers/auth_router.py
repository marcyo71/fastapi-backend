from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from backend.auth import create_access_token

router = APIRouter()

# Pagina di login semplice (HTML)
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return """
    <html>
        <body>
            <h2>Login</h2>
            <form action="/login" method="post">
                <input type="text" name="username" placeholder="Username" required />
                <input type="password" name="password" placeholder="Password" required />
                <button type="submit">Accedi</button>
            </form>
        </body>
    </html>
    """

# Gestione login con JWT
@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "segreto":
        token = create_access_token({"sub": username, "role": "admin"})
        response = RedirectResponse(url="/admin", status_code=303)
        response.set_cookie(
            key="session",
            value=token,
            httponly=True,
            samesite="Lax",
            max_age=3600,
            path="/"
        )
        return response

    elif username == "marcy" and password == "123":
        token = create_access_token({"sub": username, "role": "user"})
        response = RedirectResponse(url="/pagamenti", status_code=303)
        response.set_cookie(
            key="session",
            value=token,
            httponly=True,
            samesite="Lax",
            max_age=3600,
            path="/"
        )
        return response

    return RedirectResponse(url="/login", status_code=303)

# Logout coerente: cancella il cookie session
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session")
    return response
