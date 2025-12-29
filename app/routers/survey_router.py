from app import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.survey_model import Survey
from app.schemas.survey_schema import SurveyCreate, SurveyOut

router = APIRouter(prefix="/surveys", tags=["Surveys"])

@router.get("/", response_model=list[SurveyOut])
def get_surveys(user_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Survey)
    if user_id:
        query = query.filter(Survey.user_id == user_id)
    return query.all()

@router.post("/", response_model=SurveyOut)
def create_survey(survey: SurveyCreate, db: Session = Depends(get_db)):
    new_survey = Survey(**survey.model_dump())
    db.add(new_survey)
    db.commit()
    db.refresh(new_survey)
    return new_survey

@router.patch("/{survey_id}", response_model=SurveyOut)
def complete_survey(survey_id: int, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    survey.completed = True
    db.commit()
    db.refresh(survey)
    return survey

