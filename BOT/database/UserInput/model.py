from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from database.core import Base


class UserInput(Base):
    __tablename__ = 'user_input'

    id = Column(Integer, primary_key=True, index=True)
    process_name = Column(String, index=True, unique=False, nullable=False)
    stage = Column(String, nullable=False)
    subprocess_name = Column(String, nullable=False)
    subprocess_guid = Column(String, nullable=False, unique=True)
    queue_name = Column(String, nullable=False, unique=True)
    queue_guid = Column(String, nullable=False, unique=True)

    # Связь с FilterTable
    filters = relationship("FilterTable", back_populates="user_input")

    def __repr__(self):
        return f"<UserInput(id={self.id}, process_name={self.process_name}, subprocess_name={self.subprocess_name}), queue_name={self.queue_name},queue_guid={self.queue_guid}>"
