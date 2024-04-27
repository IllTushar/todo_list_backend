from sqlalchemy import INTEGER, VARCHAR, Column
from ..db_connection.database_connection import Base


class User(Base):
    __tablename__ = 'user_info'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR)
    email = Column(VARCHAR, unique=True)
    description = Column(VARCHAR, nullable=True)
