from pydantic import BaseModel

class StudentInput(BaseModel):
    GPA: float
    Final_Exam_Scores: float
    Hours_of_Study_per_Week: float
    Attendance_Rate: float
    Mental_Health_Status: str 
    Participation_in_Extracurricular_Activities: int
    Family_Income: float

class UniversityAdmissionInput(BaseModel):
    High_School_GPA: float
    Final_Exam_Scores: float
    Hours_of_Study_per_Week: float
    Attendance_Rate: float
    Mental_Health_Status: str
    Participation_in_Extracurricular_Activities: int
    Family_Income: float