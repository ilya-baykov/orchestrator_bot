from sqlalchemy import Column, BigInteger, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship

from database.core import Base


class OrchestratorQueues(Base):
    __tablename__ = 'queues'  # Имя таблицы
    __table_args__ = {'schema': 'orchestrator'}  # Указываем схему

    id = Column(BigInteger, primary_key=True)  # id записи в таблице
    guid = Column(String, nullable=True)  # GUID очереди
    name = Column(String, nullable=True)  # Имя очереди
    description = Column(Text, nullable=True)  # Описание очереди
    created = Column(TIMESTAMP, nullable=False)  # Дата создания
    updated = Column(TIMESTAMP, nullable=False)  # Дата обновления
    is_deleted = Column(Integer, nullable=False)  # Флаг удаления
    account_id = Column(BigInteger, nullable=True)  # ID аккаунта
    auto_repeat_application = Column(Integer, nullable=False)  # Автоматическое повторение приложения
    auto_repeat_business = Column(Integer, nullable=False)  # Автоматическое повторение бизнеса
    max_repeat = Column(BigInteger, nullable=False)  # Максимальное количество повторений
    change_to_status_abandoned_task_from_created_via = Column(BigInteger,
                                                              nullable=False)  # Изменение статуса заброшенной задачи из созданного
    change_to_status_abandoned_task_from_in_progress_via = Column(BigInteger,
                                                                  nullable=False)  # Изменение статуса заброшенной задачи из процесса
    auto_change_status = Column(Integer, nullable=False)  # Автоматическое изменение статуса
    auto_repeat_abandoned = Column(Integer, nullable=False)  # Автоматическое повторение заброшенных задач
    unique_tasks = Column(Integer, nullable=False)  # Уникальные задачи

    # Определяем отношение
    tasks = relationship('OrchestratorTasks', back_populates='queue')

    def __repr__(self):
        return (f"<OrchestratorQueues(id={self.id}, guid={self.guid}, name={self.name}, "
                f"description={self.description}, created={self.created}, updated={self.updated})>")
