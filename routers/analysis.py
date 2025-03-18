import os

from fastapi import APIRouter

from lib.apis.Analysis import extract_text_from_pdf, analyze_blood_test
from lib.models.AnalysisResult import AnalysisResult
from fastapi import HTTPException
from fastapi import File, Form, UploadFile

from lib.utilities.email import send_email_with_results

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.get("/")
async def base_analysis():
    return {"Hello": "Analysis"}

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_blood_test_endpoint(pdf_file: UploadFile = File(...), arabic: bool = Form(False), email: str = Form(...)):
    if pdf_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    blood_test_text = extract_text_from_pdf(pdf_file)
    analysis_dict = analyze_blood_test(blood_test_text, arabic)

    try:
        send_email_with_results(email, analysis_dict, arabic)
        return AnalysisResult(**analysis_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing Gemini response: {e}")

# @router.post("/analyze", response_model=AnalysisResult)
# async def analyze_blood_test_endpoint(pdf_file: UploadFile = File(...), arabic: bool = Form(False)):
#     if pdf_file.content_type != "application/pdf":
#         raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
#
#     blood_test_text = extract_text_from_pdf(pdf_file)
#     analysis_dict = analyze_blood_test(blood_test_text, arabic)
#
#     try:
#         return AnalysisResult(**analysis_dict)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing Gemini response: {e}")