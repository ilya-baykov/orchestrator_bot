from sqlalchemy.orm import relationship

from database.core import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, CheckConstraint
import enum


# Определяем перечисление для допустимых значений
class FiltrationPeriodEnum(enum.Enum):
    HOUR = "Час"
    DAY = "День"
    WEEKLY = "Неделя"
    MONTH = 'Месяц'
    YEAR = 'Год'


class FilterTable(Base):
    __tablename__ = 'filter_table'

    id = Column(Integer, primary_key=True)  # Уникальный идентификатор записи (первичный ключ).
    fk_id = Column(Integer, ForeignKey('user_input.id'))  # Внешний ключ, ссылающийся на таблицу user_input.

    department_access = Column(String, nullable=False)  # Строка, указывающая доступность для определенного отдела.
    filtration_period = Column(String, nullable=False)  # Строка, хранящая варианты периодов фильтрации.

    user_input = relationship("UserInput", back_populates="filters")

    __table_args__ = (
        CheckConstraint(
            # Проверка формата значения filtration_period:
            # 1) Строка должна начинаться с одного из указанных значений.
            # 2) После первого значения могут следовать ноль или более

            "LOWER(filtration_period) ~ '^(час|день|неделя|месяц|год)(;\\s*(час|день|неделя|месяц|год))*$'",
            name='check_filtration_period'
        ),
    )
