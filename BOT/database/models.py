from sqlalchemy import Column, Integer, String

from database.core import Base


class User(Base):
    __tablename__ = 'users'  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)  # Поле ID
    username = Column(String, unique=True, index=True)  # Поле для имени пользователя
    email = Column(String, unique=True, index=True)  # Поле для электронной почты
    full_name = Column(String, nullable=True)  # Поле для полного имени

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
