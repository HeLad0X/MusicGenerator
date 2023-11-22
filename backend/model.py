from sqlalchemy import Boolean, Column, Integer, String, Date, Text

from database import Base

class File(Base):
    __tablename__ = 'Project'

    project_id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String)
    preprocessing_status = Column(Boolean)
    create_time = Column(Date,nullable=True)
    description = Column(Text,nullable=True)