from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.db.engine import Base
from datetime import datetime

class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    inviter_id = Column(Integer, ForeignKey("users.id"), nullable=False)   # chi invita
    invited_id = Column(Integer, ForeignKey("users.id"), nullable=False)   # chi viene invitato
    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔗 Relazioni con User
    inviter = relationship("User", foreign_keys=[inviter_id], backref="sent_referrals")
    invited = relationship("User", foreign_keys=[invited_id], backref="received_referrals")

    def __repr__(self):
        return f"<Referral(inviter={self.inviter_id}, invited={self.invited_id})>"
