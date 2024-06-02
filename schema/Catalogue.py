from pydantic import BaseModel


class CatalogueCourse(BaseModel):
    subject:str # ABST
    course_code: int #1100
    credits: float # 3.0
    hours: dict[str, float] # {"lecture" : 3, "seminar" : 0, "lab" : 0}
    title: str #  Canadian Aboriginal Experience 
    description: str # not pasting the whole description here
    
    # this is really the proper way to do it???
    def __init__(__pydantic_self__, **data: any) -> None:
        super().__init__(**data)

class Catalogue(BaseModel):
    courses:list[CatalogueCourse] = []

    def __init__(__pydantic_self__, **data: any) -> None:
        super().__init__(**data)
    
    