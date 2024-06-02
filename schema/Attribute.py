from pydantic import BaseModel
import json 
import os


class Attribute(BaseModel):
    subject: str
    course_code: int
    attributes: dict[str, bool] # could use 'attributes' here but it bugs out
    
    def __init__(__pydantic_self__, **data: any) -> None:
        super().__init__(**data)

class Attributes(BaseModel):
    attributes:list[Attribute]
    
    def __init__(__pydantic_self__, **data: any) -> None:
        super().__init__(**data)
        