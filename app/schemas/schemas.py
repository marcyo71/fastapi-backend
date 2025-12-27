from pydantic import BaseModel, constr

class UserCreate(BaseModel):
    email: str
    password: constr(min_length=8, max_length=64)  # vincolo di lunghezza

class Token(BaseModel):
    access_token: str
    token_type: str

class UserOut(BaseModel):
    id: int
    email: str
    is_active: bool
