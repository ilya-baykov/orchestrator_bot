from sqlalchemy import Column, String, Integer

from database.core import Base


class UserInput(Base):
    __tablename__ = 'user_input'

    id = Column(Integer, primary_key=True, index=True)  # id записи в таблице
    process_name = Column(String, index=True, unique=False, nullable=False)  # Имя робота/проекта
    stage = Column(String, nullable=False)  # Этап процесса
    subprocess_name = Column(String, nullable=False)  # Имя процесса
    subprocess_guid = Column(String, nullable=False, unique=True)  # Guid процесса
    queue_name = Column(String, nullable=False, unique=True)  # Имя очереди процесса
    queue_guid = Column(String, nullable=False, unique=True)  # Guid очереди
    department_access = Column(String, nullable=False)  # Указывается доступность определённому отделу

    def __repr__(self):
        return f"<UserInput(id={self.id}, process_name={self.process_name},subprocess_name={self.subprocess_name})>"
