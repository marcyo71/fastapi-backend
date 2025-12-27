from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    reward = Column(Float, nullable=False)  # ✅ aggiunto

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="surveys")
