from sqlalchemy import Column, Integer, String

from database.core import Base


class TelegramUser(Base):
    __tablename__ = 'telegram_users'  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)  # Поле ID
    telegram_username = Column(String, unique=True, index=True)  # Поле для имени пользователя
    telegram_id = Column(String, unique=True, index=True)  # Поле для id телеграмм пользователя

    def __repr__(self):
        return f"<User(id={self.id}, telegram_username={self.telegram_username})>"
