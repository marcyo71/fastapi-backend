from pydantic import BaseModel

class SurveyCreate(BaseModel):
    title: str
    reward: float
    user_id: int

class SurveyOut(SurveyCreate):
    id: int
    completed: bool

    class Config:
        from_attributes = True  # Pydantic v2
