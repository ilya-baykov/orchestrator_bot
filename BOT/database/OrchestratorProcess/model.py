from sqlalchemy import Column, Integer, String

from database.core import Base


class OrchestratorProcess(Base):
    __tablename__ = 'orchestrator_processes'  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)  # Поле ID
    process_name = Column(String, nullable=False, unique=True)
    process_guid = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<OrchestratorProcess(id={self.id}, process_name={self.process_name})>"
