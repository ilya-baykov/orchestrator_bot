from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.core import Base


class TelegramUser(Base):
    __tablename__ = 'telegram_users'

    id = Column(Integer, primary_key=True, index=True)
    access_list_id = Column(ForeignKey("access_list.id"))
    telegram_username = Column(String, unique=True, index=True)
    telegram_id = Column(String, unique=True, index=True)

    access_list = relationship("AccessList", back_populates="telegram_users")

    def __repr__(self):
        return f"<User(id={self.id}, telegram_username={self.telegram_username})>"
