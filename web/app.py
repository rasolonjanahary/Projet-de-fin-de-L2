from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
import re

class Etudiant(BaseModel):
    GRE_Score: float
    TOEFL_Score: float
    University_Rating: int
    SOP: float
    LOR : float
    CGPA: float
    Research: int


app = FastAPI(title="Prédicteur de chance d'admission des étudiants")
templates = Jinja2Templates(directory="templates")

model = joblib.load("../models/logistic.pkl")
model_reg = joblib.load("../models/linear.pkl")

@app.get("/form_cla", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.get("/form_reg", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form1.html", {"request": request})

@app.post("/predict_cla", response_class=HTMLResponse)
async def predire_chance_admission(
    request: Request,
    GRE_Score: float = Form(...),
    TOEFL_Score: float = Form(...),
    University_Rating: int = Form(...),
    SOP: float = Form(...),
    LOR: float = Form(...),
    CGPA: float = Form(...),
    Research: int = Form(...)
    ):

    input_data = {
        "GRE Score": GRE_Score,
        "TOEFL Score": TOEFL_Score,
        "University Rating": University_Rating,
        "SOP": SOP,
        "LOR ": LOR,
        "CGPA": CGPA,
        "Research": Research
    }
    
    input_df = pd.DataFrame([input_data])
    
    # Prédiction
    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0].tolist() if hasattr(model, "predict_proba") else None
    return templates.TemplateResponse(
        "resultat.html",
        {
            "request": request,
            "prediction": int(prediction),
            "probability": round(proba[1] * 100, 2) if proba else None ,
            "probability1": round(proba[0] * 100, 2) if proba else None ,
            "message": "Vous êtes admis" if prediction == 1 else "Vous n'êtes pas admis"
        }
    )


@app.post("/predict_reg", response_class=HTMLResponse)
async def predire_chance_admission_reg(
    request: Request,
    GRE_Score: float = Form(...),
    TOEFL_Score: float = Form(...),
    University_Rating: int = Form(...),
    SOP: float = Form(...),
    LOR: float = Form(...),
    CGPA: float = Form(...),
    Research: int = Form(...)
    ):

    input_data = {
        "GRE Score": GRE_Score,
        "TOEFL Score": TOEFL_Score,
        "University Rating": University_Rating,
        "SOP": SOP,
        "LOR ": LOR,
        "CGPA": CGPA,
        "Research": Research
    }
    
    input_df = pd.DataFrame([input_data])
    
    # Prédiction
    prediction = model_reg.predict(input_df)[0]

    return templates.TemplateResponse(
        "resultat1.html",
        {
            "request": request,
            "prediction": round(float(prediction), 2) * 100,
            "prediction_c": round(1 - round(float(prediction), 2), 2) * 100,
            "message": "Vous êtes admis" if prediction == 1 else "Vous n'êtes pas admis"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)