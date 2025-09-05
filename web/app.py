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

model = joblib.load("../models/logistic_1.pkl")
model_reg = joblib.load("../models/linear.pkl")

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# @app.get("/form_reg", response_class=HTMLResponse)
# async def form_page(request: Request):
#     return templates.TemplateResponse("form1.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
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

    gre = GRE_Score if GRE_Score is not None and 260 <= GRE_Score <= 340 else 300
    toefl = TOEFL_Score if TOEFL_Score is not None and 0 <= TOEFL_Score <= 120 else 90
    ur = University_Rating if University_Rating is not None and 1 <= University_Rating <= 5 else 3
    sop = SOP if SOP is not None and 0.0 <= SOP <= 5.0 else 3.0
    lor = LOR if LOR is not None and 0.0 <= LOR <= 5.0 else 3.0
    cgpa = CGPA if CGPA is not None and 0.0 <= CGPA <= 10.0 else 7.5
    research = Research if Research in [0, 1] else 0

    input_data = {
        "GRE Score": gre,
        "TOEFL Score": toefl,
        "University Rating": ur,
        "SOP": sop,
        "LOR ": sop,
        "CGPA": cgpa,
        "Research": research
    }
    
    input_df = pd.DataFrame([input_data])
    
    # Prédiction
    prediction = model.predict(input_df)[0]
    prediction_reg = model_reg.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0].tolist() if hasattr(model, "predict_proba") else None
    return templates.TemplateResponse(
        "resultat.html",
        {
            "request": request,
            "prediction": int(prediction),
            "probability": round(proba[1] * 100, 2) if proba else None ,
            "probability1": round(proba[0] * 100, 2) if proba else None ,
            "prediction_reg": round(float(prediction_reg), 2) * 100,
            "prediction_reg_c": round(1 - round(float(prediction_reg), 2), 2) * 100,
            "message": "Vous êtes admis" if prediction == 1 else "Vous n'êtes pas admis"
        }
    )


# @app.post("/predict_reg", response_class=HTMLResponse)
# async def predire_chance_admission_reg(
#     request: Request,
#     GRE_Score: float = Form(...),
#     TOEFL_Score: float = Form(...),
#     University_Rating: int = Form(...),
#     SOP: float = Form(...),
#     LOR: float = Form(...),
#     CGPA: float = Form(...),
#     Research: int = Form(...)
#     ):

#     gre = GRE_Score if GRE_Score is not None and 260 <= GRE_Score <= 340 else 300
#     toefl = TOEFL_Score if TOEFL_Score is not None and 0 <= TOEFL_Score <= 120 else 90
#     ur = University_Rating if University_Rating is not None and 1 <= University_Rating <= 5 else 3
#     sop = SOP if SOP is not None and 0.0 <= SOP <= 5.0 else 3.0
#     lor = LOR if LOR is not None and 0.0 <= LOR <= 5.0 else 3.0
#     cgpa = CGPA if CGPA is not None and 0.0 <= CGPA <= 10.0 else 7.5
#     research = Research if Research in [0, 1] else 0

#     input_data = {
#         "GRE Score": gre,
#         "TOEFL Score": toefl,
#         "University Rating": ur,
#         "SOP": sop,
#         "LOR ": sop,
#         "CGPA": cgpa,
#         "Research": research
#     }
    
#     input_df = pd.DataFrame([input_data])
    
#     # Prédiction
#     prediction = model_reg.predict(input_df)[0]

#     return templates.TemplateResponse(
#         "resultat1.html",
#         {
#             "request": request,
#             "prediction": round(float(prediction), 2) * 100,
#             "prediction_c": round(1 - round(float(prediction), 2), 2) * 100,
#             "message": "Vous êtes admis" if prediction == 1 else "Vous n'êtes pas admis"
#         }
#     )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)