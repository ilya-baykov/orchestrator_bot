from sqlalchemy import Column, Integer, String

from database.core import Base


class AccessList(Base):
    __tablename__ = 'access_list'

    id = Column(Integer, primary_key=True, index=True)  # Поле ID
    fullname = Column(String)  # Поле с ФИО сотрудника
    phone = Column(String, unique=True)  # Поле для телефона, привязанному к аккаунту в телеграмм

    def __repr__(self):
        return f"<AccessList(id={self.id}, phone={self.phone})>"
