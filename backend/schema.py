from pydantic import BaseModel
from datetime import date

class Project(BaseModel):
    project_id : int
    project_name : str
    preprocessing_status : bool
    create_time : date
    description : str

    class Config:
        orm_mode = True