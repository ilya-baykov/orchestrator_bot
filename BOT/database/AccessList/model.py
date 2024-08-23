from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.core import Base


class AccessList(Base):
    __tablename__ = 'access_list'

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    phone = Column(String, unique=True)
    department = Column(String, nullable=False)

    telegram_users = relationship("TelegramUser", back_populates="access_list")

    def __repr__(self):
        return f"<AccessList(id={self.id}, phone={self.phone})>"
