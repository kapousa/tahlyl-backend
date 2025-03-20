import os
from typing import List

from fastapi import APIRouter
from pdfminer.high_level import extract_text

from lib.apis.Analysis import extract_text_from_pdf, analyze_blood_test, compare_reports
from lib.models.AnalysisResult import AnalysisResult
from fastapi import HTTPException
from fastapi import File, Form, UploadFile

from lib.models.CompareReports import CompareReports
from lib.utilities.email import send_analysis_results_email, send_compare_report_email

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/")
async def base_analysis():
    return {"Hello": "Analysis"}


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_blood_test_endpoint(pdf_file: UploadFile = File(...), arabic: bool = Form(False),
                                      email: str = Form(...)):
    if pdf_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    blood_test_text = extract_text_from_pdf(pdf_file)
    analysis_dict = analyze_blood_test(blood_test_text, arabic)

    try:
        send_analysis_results_email(email, analysis_dict, arabic)
        return AnalysisResult(**analysis_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing Gemini response: {e}")


@router.post("/compare", response_model=CompareReports)
async def compare_blood_tests(
        files: List[UploadFile] = File(...),
        arabic: bool = Form(False), email: str = Form(...)):
    """Compares multiple blood test reports with language option."""
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="Please upload at least two files.")

    reports = []
    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
        reports.append(extract_text(file.file))
    try:
        result = compare_reports(reports, arabic) # result is now a dict.
        send_compare_report_email(email, result['summary'], arabic)
        return CompareReports(**result) # Unpack the dictionary into the CompareReports model.
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing Gemini response: {e}")