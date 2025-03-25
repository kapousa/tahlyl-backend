# analysis.py
import os
from typing import List, Union

from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from pdfminer.high_level import extract_text

from lib.apis.Analysis import extract_text_from_pdf, analyze_blood_test, compare_reports
from lib.models.AnalysisResult import AnalysisResult
from lib.models.CompareReports import CompareReports
from lib.utils.email import send_analysis_results_email, send_compare_report_email
from lib.utils.logger import logger
#
router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.get("/")
async def base_analysis():
    logger.info("Base analysis endpoint hit.")
    return {"Hello": "Analysis"}

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_blood_test_endpoint(pdf_file: UploadFile = File(...), arabic: bool = Form(False),
                                      email: str = Form(...), tone: str = Form(...)):
    logger.info(f"Analyze blood test endpoint hit. Email: {email}, Arabic: {arabic}, Tone: {tone}")
    tone = tone.lower()
    try:
        if pdf_file.content_type != "application/pdf":
            logger.error("Invalid file type. Only PDF files are allowed.")
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

        blood_test_text = extract_text_from_pdf(pdf_file)
        analysis_dict = analyze_blood_test(blood_test_text, arabic, tone)

        send_analysis_results_email(email, analysis_dict, arabic, tone)
        logger.info(f"Email sent successfully to {email}.")
        return AnalysisResult(**analysis_dict)

    except HTTPException as e:
        logger.error(f"HTTPException: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error processing Gemini response: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing Gemini response: {e}")

@router.post("/compare", response_model=CompareReports)
async def compare_blood_tests(
        files: List[UploadFile] = File(...),
        arabic: bool = Form(False), email: str = Form(...)):
    logger.info(f"Compare blood tests endpoint hit. Email: {email}, Arabic: {arabic}")
    try:
        if len(files) < 2:
            logger.error("Please upload at least two files.")
            raise HTTPException(status_code=400, detail="Please upload at least two files.")

        reports = []
        for file in files:
            if file.content_type != "application/pdf":
                logger.error("Invalid file type. Only PDF files are allowed.")
                raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
            reports.append(extract_text(file.file))

        result = compare_reports(reports, arabic)
        send_compare_report_email(email, result['summary'], arabic)
        logger.info(f"Email sent successfully to {email}.")
        return CompareReports(**result)

    except HTTPException as e:
        logger.error(f"HTTPException: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error processing Gemini response: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing Gemini response: {e}")