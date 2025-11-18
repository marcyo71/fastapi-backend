from pydantic import BaseModel

class StatusResponse(BaseModel):
    status: str

    class Config:
        orm_mode = True
