from pydantic import BaseModel
import json
import os

class Transfer(BaseModel):
    subject:str
    course_code:int
    source:str = "LANG"
    destination:str
    credit:str
    effective_start:str
    effective_end:str | None
    
    def __init__(__pydantic_self__, **data: any) -> None:
        super().__init__(**data)
        
    
    class Config:
        schema_extra = {
            "example1": {
                 "subject": "CPSC",
                "course_code": 1050,
                "source": "LANG",
                "destination": "ALEX",
                "credit": "ALEX CPSC 1XX (3)",
                "effective_start": "Sep/15",
                "effective_end": "present"
            },
            "example2": {
                "subject": "CPSC",
                "course_code": 1050,
                "source": "LANG",
                "destination": "AU",
                "credit": "AU COMP 2XX (3)",
                "effective_start": "May/15",
                "effective_end": "present"
            }
        }
        
        
        
    
class Transfers(BaseModel):
    courses:list[Transfer]

    def __init__(__pydantic_self__, **data: any) -> None:
        super().__init__(**data)
        
    def toJSON(self):
        # ugly but neccessary to pretty print the json file
        return json.dumps(json.loads(self.json()), default=vars, indent=4)
    
    def saveToFile(self):
        
        file_location = f"data/transfer/transfers.json"
        
        # create dir if it doesn't exist
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        
        with open(file_location, "w+") as fi:
            fi.write(self.toJSON())
