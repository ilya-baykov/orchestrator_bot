from sqlalchemy import Column, BigInteger, String, Text, Integer, TIMESTAMP

from database.core import Base


class OrchestratorTasks(Base):
    __tablename__ = 'tasks'  # Имя таблицы
    __table_args__ = {'schema': 'orchestrator'}  # Указываем схему

    id = Column(BigInteger, primary_key=True)  # id записи в таблице
    guid = Column(String, nullable=True)  # GUID задачи
    queue_id = Column(BigInteger, nullable=True)  # ID очереди
    name = Column(String, nullable=True)  # Название задачи
    description = Column(Text, nullable=True)  # Описание задачи
    status = Column(Integer, nullable=True)  # Статус задачи
    job_id = Column(BigInteger, nullable=True)  # ID работы
    priority = Column(Integer, nullable=False)  # Приоритет задачи
    parameters = Column(Text, nullable=True)  # Параметры задачи
    created = Column(TIMESTAMP, nullable=False)  # Дата создания
    started = Column(TIMESTAMP, nullable=True)  # Дата начала
    postponed = Column(TIMESTAMP(timezone=True), nullable=True)  # Дата отложенной задачи
    deadline = Column(TIMESTAMP, nullable=True)  # Дата завершения
    updated = Column(TIMESTAMP, nullable=False)  # Дата обновления
    comment = Column(Text, nullable=True)  # Комментарий
    is_deleted = Column(Integer, nullable=False)  # Флаг удаления
    account_id = Column(BigInteger, nullable=True)  # ID аккаунта
    tags = Column(Text, nullable=True)  # Теги задачи
    retries = Column(BigInteger, nullable=False)  # Количество попыток
    parent_task = Column(String, nullable=True)  # ID родительской задачи

    def __repr__(self):
        return f"<OrchestratorTasks(id={self.id}, guid={self.guid}, status={self.status})>"
