from app import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.survey_model import Survey

router = APIRouter(
    prefix="/survey-results",
    tags=["survey-results"],
    dependencies=[Depends(get_db)]
)

@router.get("/by-user/{user_id}")
def get_surveys_by_user(user_id: int, db: Session):
    surveys = db.query(Survey).filter(Survey.user_id == user_id).all()
    return [{"id": s.id, "title": s.title, "reward": s.reward} for s in surveys]

@router.get("/total-reward/{user_id}")
def get_total_reward(user_id: int, db: Session):
    total = db.query(Survey).filter(Survey.user_id == user_id).with_entities(Survey.reward).all()
    reward_sum = sum(r[0] for r in total)
    return {"user_id": user_id, "total_reward": reward_sum}

