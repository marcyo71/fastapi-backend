from backend.models.survey_model import Survey
from sqlalchemy.orm import Session
from backend.db import Base

def create_survey(data: dict, db: Session) -> Survey:
    survey = Survey(**data)
    db.add(survey)
    db.commit()
    db.refresh(survey)
    return survey

def get_all_surveys(db: Session) -> list[Survey]:
    return db.query(Survey).all()
