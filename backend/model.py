from sqlalchemy import Boolean, Column, Integer, String

from database import Base

class File(Base):
    __tablename__ = 'file_desc'

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)