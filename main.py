from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import pandas as pd
from schemas import StudentInput, UniversityAdmissionInput
from fastapi import APIRouter

app = FastAPI(title="Student Performance Predictor")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Charger le pipeline
model_gpa = joblib.load("models/model_gpa.pkl")
model_hsgpa = joblib.load("models/model_hsgpa.pkl")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/change-school", response_class=HTMLResponse)
async def get_change_school_form(request: Request):
    return templates.TemplateResponse("change_school.html", {"request": request})

@app.post("/change-school", response_class=HTMLResponse)
async def post_change_school_form(
    request: Request,
    GPA: float = Form(...),
    Final_Exam_Scores: float = Form(...),
    Hours_of_Study_per_Week: float = Form(...),
    Attendance_Rate: float = Form(...),
    Mental_Health_Status: str = Form(...),
    Participation_in_Extracurricular_Activities: str = Form(...),
    Family_Income: float = Form(...)
):
    data = StudentInput(
        GPA=GPA,
        Final_Exam_Scores=Final_Exam_Scores,
        Hours_of_Study_per_Week=Hours_of_Study_per_Week,
        Attendance_Rate=Attendance_Rate,
        Mental_Health_Status=Mental_Health_Status,
        Participation_in_Extracurricular_Activities=Participation_in_Extracurricular_Activities,
        Family_Income=Family_Income
    )

    input_df = pd.DataFrame([{
        "GPA": data.GPA,
        "Final Exam Scores": data.Final_Exam_Scores,
        "Hours of Study per Week": data.Hours_of_Study_per_Week,
        "Attendance Rate": data.Attendance_Rate,
        "Mental Health Status": data.Mental_Health_Status,
        "Participation in Extracurricular Activities": data.Participation_in_Extracurricular_Activities,
        "Family Income": data.Family_Income
    }])

    prediction = int(model_gpa.predict(input_df)[0])
    return templates.TemplateResponse("change_school.html", {
        "request": request,
        "prediction": prediction
    })


@app.get("/university-admission", response_class=HTMLResponse)
async def get_university_admission_form(request: Request):
    return templates.TemplateResponse("university_admission.html", {"request": request})

@app.post("/university-admission", response_class=HTMLResponse)
async def post_university_admission_form(
    request: Request,
    High_School_GPA: float = Form(...),
    Final_Exam_Scores: float = Form(...),
    Hours_of_Study_per_Week: float = Form(...),
    Attendance_Rate: float = Form(...),
    Mental_Health_Status: str = Form(...),
    Participation_in_Extracurricular_Activities: str = Form(...),
    Family_Income: float = Form(...)
):
    data = UniversityAdmissionInput(
        High_School_GPA=High_School_GPA,
        Final_Exam_Scores=Final_Exam_Scores,
        Hours_of_Study_per_Week=Hours_of_Study_per_Week,
        Attendance_Rate=Attendance_Rate,
        Mental_Health_Status=Mental_Health_Status,
        Participation_in_Extracurricular_Activities=Participation_in_Extracurricular_Activities,
        Family_Income=Family_Income
    )

    input_df = pd.DataFrame([{
        "High School GPA": data.High_School_GPA,
        "Final Exam Scores": data.Final_Exam_Scores,
        "Hours of Study per Week": data.Hours_of_Study_per_Week,
        "Attendance Rate": data.Attendance_Rate,
        "Mental Health Status": data.Mental_Health_Status,
        "Participation in Extracurricular Activities": data.Participation_in_Extracurricular_Activities,
        "Family Income": data.Family_Income
    }])

    prediction = int(model_hsgpa.predict(input_df)[0])
    return templates.TemplateResponse("admission_universitaire.html", {
        "request": request,
        "prediction": prediction
    })