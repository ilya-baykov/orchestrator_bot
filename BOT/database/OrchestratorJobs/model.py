from sqlalchemy import Column, BigInteger, Integer, String, DateTime, TIMESTAMP
from database.core import Base


class OrchestratorJobs(Base):
    __tablename__ = 'jobs'  # Имя таблицы
    __table_args__ = {'schema': 'orchestrator'}  # Указываем схему

    id = Column(BigInteger, primary_key=True)  # id записи в таблице
    guid = Column(String, nullable=True)  # GUID задачи (изменено на String, так как character может быть ограничен)
    robot_id = Column(BigInteger, nullable=True)  # ID робота
    process_version_id = Column(BigInteger, nullable=True)  # ID версии процесса
    task_id = Column(BigInteger, nullable=True)  # ID задачи
    status = Column(Integer, nullable=True)  # Статус задачи
    created = Column(TIMESTAMP, nullable=False)  # Дата создания
    updated = Column(TIMESTAMP, nullable=False)  # Дата обновления
    started = Column(TIMESTAMP, nullable=True)  # Дата начала
    finished = Column(TIMESTAMP(timezone=True), nullable=True)  # Дата завершения (с учетом часового пояса)
    stop_after = Column(TIMESTAMP, nullable=True)  # Дата остановки
    abort_after = Column(TIMESTAMP, nullable=True)  # Дата прерывания
    is_deleted = Column(Integer, nullable=False)  # Флаг удаления
    account_id = Column(BigInteger, nullable=True)  # ID аккаунта
    schedule_id = Column(BigInteger, nullable=True)  # ID расписания
    robot_group_id = Column(Integer, nullable=True)  # ID группы роботов

    def __repr__(self):
        return f"<OrchestratorJobs(id={self.id}, guid={self.guid}, status={self.status})>"
