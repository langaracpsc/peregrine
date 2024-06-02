from pydantic import BaseModel, Field
from enum import Enum, IntEnum

from datetime import date, datetime
import os
import json
import logging

class scheduleTypes(Enum):
    _ = " "
    
    Lecture = "Lecture"
    Lab = "Lab"
    Seminar = "Seminar"
    Practicum = "Practicum"
    Tutorial = "Tutorial"
    WWW = "WWW"
    Exam = "Exam"
    
    GIS_Guided_Independent_Study = "GIS Guided Independent Study"
    Flexible_Assessment = "Flexible Assessment"
    Field_School = "Field School"
    On_Site_Work = "On Site Work"
    Exchange_International = "Exchange-International"
    COOP = "CO-OP(on site work experience)"
    
    

class ScheduleEntry(BaseModel):
    type: 'scheduleTypes'   = Field(description='Type of the section.')
    days: str               = Field(description='Days of the week of the session e.g. ```M-W----```.')
    time: str               = Field(description='Time session starts and ends e.g. ```1030-1220```.')
    start: str | None       = Field(description='Date session starts (```YYYY-MM-DD```).')
    end: str | None         = Field(description='Date session ends (```YYYY-MM-DD```).')
    room: str               = Field(description='Room session is in.')
    instructor: str         = Field(description='Instructor(s) for this session.')
    
    class Config:
        schema_extra = {
            "example": {
                "type" : "Lecture",
                "days" : "M-W----",
                "time" : "1030-1220",
                "start": None,
                "end" : None,
                "room": "A136B",
                "instructor": "Adam Solomonian"
            }
        }
# https://langara.ca/reg-guide/before-you-register/search-for-courses.html

class RPEnum(Enum):
    R = "R"
    P = "P"
    RP = "RP"

class seatsEnum(Enum):
    inactive = "Inact" # registration not open yet
    cancel = "Cancel" # course cancelled

class waitlistEnum(Enum):
    no_waitlist = "N/A" # course does not have a waitlist
    full = "Full"
    

class Course(BaseModel):
    RP : RPEnum | None                  = Field(description='Prerequisites of the course.')
    seats: int | seatsEnum              = Field(description='```"Inact"``` means registration isn\'t open yet. \n\n```"Cancel"``` means that the course is cancelled.')
    waitlist: int | waitlistEnum | None = Field(description='```null``` means that the course has no waitlist (ie MATH 1183 & MATH 1283). \n\n```"N/A"``` means the course does not have a waitlist.')
    crn: int                            = Field(description="Always 5 digits long.")
    subject: str                        = Field(description="Subject area e.g. ```CPSC```.")
    course_code: int                    = Field(description="Course code e.g. ```1050```.")
    section: str                        = Field(description="Section e.g. ```001```, ```W01```, ```M01```.")
    credits: float                      = Field(description="Credits the course is worth.")
    title: str                          = Field(description="Title of the course e.g. ```Intro to Computer Science```.")
    add_fees: float | None              = Field(description="Additional fees (in dollars).")
    rpt_limit: int | None               = Field(description="Repeat limit. There may be other repeat limits not listed here you should keep in mind.")
    notes: str | None                   = Field(description="Notes for a section.")
    schedule:list[ScheduleEntry]        = Field(description="Times that the course meets.")
    
    yearsemester: str | None  # used internally 
    
    def __str__(self):
        return f"Course: {self.subject} {self.course} CRN: {self.crn}"
    
    class Config:
        schema_extra = {
            "example": {
                "RP" : None,
                "seats" : 8,
                "waitlist" : 25,
                "crn" : 20533,
                "subject" : "ANTH",
                "course" : 1120,
                "section" : "001",
                "credits" : 3.00,
                "title" : "Intro to Cultural Anthropology",
                "add_fees" : 0,
                "rpt_limit" : None,
                "notes" : None,
                "schedule" : [ScheduleEntry.Config.schema_extra["example"]],
            }
        }

class Semesters(IntEnum):
    spring = 10
    summer = 20
    fall = 30

class Years(IntEnum):
    _2023 = 2023
    _2022 = 2022
    _2021 = 2021
    _2020 = 2020
    _2019 = 2019
    _2018 = 2018
    _2017 = 2017
    _2016 = 2016
    _2015 = 2015
    _2014 = 2014
    _2013 = 2013
    _2012 = 2012
    _2011 = 2011
    _2010 = 2010
    _2009 = 2009
    _2008 = 2008
    _2007 = 2007
    _2006 = 2006
    _2005 = 2005
    _2004 = 2004
    _2003 = 2003
    _2002 = 2002
    _2001 = 2001
    _2000 = 2000
    

class Semester(BaseModel):
    datetime_retrieved: str = Field(
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), #iso standards aren't real
        description='Date data was retrieved.'
        )
    
    year: Years                     = Field(description='Year of semester.')
    semester: Semesters             = Field(description='Term of semester')
    courses_first_day: date | None  = Field(description='Date semester courses start. This is a best estimate and should not be taken as fact.')
    courses_last_day: date | None   = Field(description='Date semester courses end. This is a best estimate and should not be taken as fact.')
    courses: list[Course]           = Field(
        default=[], 
        description='List of courses in semester.'
        )
    
    # this is really the proper way to do it???
    def __init__(__pydantic_self__, **data: any) -> None:
        super().__init__(**data)
        
    class Config:
        schema_extra = {
            "example": {
                "datetime_retrieved" : "2023-04-04",
                "year": Years._2023,
                "semester" : Semesters.spring,
                "courses_first_day" : "2023-5-08",
                "courses_last_day" : "2023-8-31",
                "courses" : [Course.Config.schema_extra["example"]]
            }
        }
    
    def addCourse(self, course:Course):
        self.courses.append(course)
    
    def courseCount(self):
        return len(self.courses)
    
    def uniqueCoursecount(self):
        uniques = []
        for c in self.courses:
            if f"{c.subject} {c.course_code}" not in uniques:
                uniques.append(f"{c.subject} {c.course_code}")
        return len(uniques)


    def __str__(self):
        s =  f"Semester data for {self.year}{self.semester}:\n"
        s += f"{self.courseCount()} sections & "
        s += f"{self.uniqueCoursecount()} unique sections.\n"
        return s
    
    def toJSON(self):
        # ugly but neccessary to pretty print the json file
        return json.dumps(json.loads(self.json()), default=vars, indent=4)
    
    def saveToFile(self, location):
        
        file_location = f"{location}/json/{self.year}{self.semester}.json"
        
        # create dir if it doesn't exist
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        
        with open(file_location, "w+") as fi:
            fi.write(self.toJSON())
    
    # sets start/end dates of semesters by looking for most common start/end dates
    # not verified to be 100% correct but should be good enough
    def extractDates(self):        
        starts = {}
        ends = {}
        
        for course in self.courses:
            for sch in course.schedule:
                
                if sch.type == "Exam":
                    continue
        
                
                if sch.start != None:
                    if sch.start not in starts:
                        starts[sch.start] = 0
                    starts[sch.start] += 1
                
                if sch.start != None:
                    if sch.end not in ends:
                        ends[sch.end] = 0
                    ends[sch.end] += 1
        
        #print(starts, "\n", ends, "\n")
        
        # get rid of impossible starts
        if self.semester == 10:
            allowed_start = [12, 1]
        if self.semester == 20:
            allowed_start = [5, 4]
        if self.semester == 30:
            allowed_start = [7, 8]
            
        for date in starts:
            month = int( date.split("-")[1] )
            if month not in allowed_start:
                starts[date] = 0
                
        # magic from stackoverflow
        s = max(starts, key=starts.get)
        
        # get rid of impossible end dates
        month_start = int(s.split("-")[1])
        for date in ends:
            month_end = int( date.split("-")[1] )
            if month_start + 1 >= month_end:
                ends[date] = 0

        e = max(ends, key=ends.get)
        
        #print(starts, "\n", ends)
        #print("start:", s)
        #print("end:", e)
        logging.info(f"Semester {self.year}{self.semester} starts on {s} and ends on {e}.")
        self.courses_first_day = s
        self.courses_last_day = e