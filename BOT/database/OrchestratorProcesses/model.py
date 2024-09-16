from sqlalchemy import Column, BigInteger, Integer, String, Text, Float, TIMESTAMP
from sqlalchemy.orm import relationship

from database.core import Base


class OrchestratorProcesses(Base):
    __tablename__ = 'processes'  # Имя таблицы
    __table_args__ = {'schema': 'orchestrator'}  # Указываем схему

    id = Column(BigInteger, primary_key=True)  # id записи в таблице
    guid = Column(String, nullable=True)  # GUID процесса
    name = Column(String, nullable=False)  # Имя процесса
    description = Column(Text, nullable=True)  # Описание процесса
    process_version_id = Column(BigInteger, nullable=True)  # ID версии процесса
    min_version_to_run_DEL = Column(String, nullable=True)  # Минимальная версия для запуска DEL
    created = Column(TIMESTAMP, nullable=False)  # Дата создания
    updated = Column(TIMESTAMP, nullable=False)  # Дата обновления
    is_deleted = Column(Integer, nullable=False)  # Флаг удаления
    account_id = Column(BigInteger, nullable=True)  # ID аккаунта
    process_type = Column(Integer, nullable=False)  # Тип процесса
    available_via_sherpa_assistant = Column(Integer, nullable=False)  # Доступно через помощника Sherpa
    min_version_to_run = Column(Float, nullable=False)  # Минимальная версия для запуска

    jobs = relationship('OrchestratorJobs', back_populates='process')

    def __repr__(self):
        return (f"<OrchestratorProcesses(id={self.id}, guid={self.guid}, name={self.name}, "
                f"description={self.description}, created={self.created}, updated={self.updated})>")
