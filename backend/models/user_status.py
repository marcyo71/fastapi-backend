from sqlalchemy import Column, Integer, String
from backend.db.engine import Base

class UserStatus(Base):
    __tablename__ = "user_status"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, unique=True, index=True)
