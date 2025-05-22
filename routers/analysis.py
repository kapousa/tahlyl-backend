# analysis.py
import json
import os
from typing import List, Union, Optional

from fastapi import APIRouter, HTTPException, File, Form, UploadFile, Depends
from pdfminer.high_level import extract_text
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config import get_db
from com.engine.analysis import report_analyzer
from com.utils.AI import analyze_report_by_gemini
from com.engine.security import get_current_user, fake_current_user
from com.schemas.result import ResultCreate
from com.utils.Helper import extract_text_from_uploaded_report
from com.schemas.analysisResult import AnalysisResult
from com.schemas.compareReports import CompareReports
from com.utils.Email import send_analysis_results_email, send_compare_report_email
from com.utils.Logger import logger
from com.utils.Report import save_report, save_analysis_result
from com.models.User import User as SQLUser

#
router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/")
async def base_analysis():
    logger.info("Base analysis endpoint hit.")
    return {"Hello": "Analysis"}


@router.post("/analyze1", response_model=AnalysisResult)
async def __analyze_blood_test_endpoint(
        pdf_file: UploadFile = File(...),
        arabic: bool = Form(False),
        email: str = Form(...),
        tone: str = Form(...),
        current_user: SQLUser = Depends(get_current_user),  # Inject the logged-in user as a parameter
        db: Session = Depends(get_db),  # Inject the database session as a parameter
):
    logger.info(
        f"Analyze blood test endpoint hit. Email: {email}, Arabic: {arabic}, Tone: {tone}, User ID: {current_user.id}")
    tone = tone.lower()
    try:
        if pdf_file.content_type != "application/pdf":
            logger.error("Invalid file type. Only PDF files are allowed.")
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

        blood_test_text = extract_text_from_uploaded_report(pdf_file)
        analysis_dict = analyze_report_by_gemini(blood_test_text)

        # Save the report using the logged-in user's ID
        report_data = {
            "name": pdf_file.filename,
            "content": blood_test_text,
        }
        report = save_report(report_data, current_user.id, db)
        logger.info(f"Report saved to database with ID: {report.id} for user: {current_user.id}")

        # Save the analysis result
        result_data = ResultCreate(
            result=analysis_dict.get("interpretation", "Analysis Result"),
            report_id=report.id,
            tone_id=tone,  # Assuming 'tone' string is what you want to save
        )
        saved_result = save_analysis_result(result_data, db)
        logger.info(f"Analysis result saved to database with ID: {saved_result.id} for report: {report.id}")

        send_analysis_results_email(email, analysis_dict, arabic, tone)
        logger.info(f"Email sent successfully to {email}.")
        return AnalysisResult(**analysis_dict)

    except HTTPException as e:
        logger.error(f"HTTPException: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error processing Gemini response or saving report: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing Gemini response or saving report: {e}")


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

        result = ""  # compare_reports(reports, arabic)
        send_compare_report_email(email, result['summary'], arabic)
        logger.info(f"Email sent successfully to {email}.")
        return CompareReports(**result)

    except HTTPException as e:
        logger.error(f"HTTPException: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error processing Gemini response: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing Gemini response: {e}")


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_report_endpoint(
        serviceId: Optional[str] = Form(None),
        reportFile: Optional[UploadFile] = File(None),
        testReportId: Optional[str] = Form(None),
        report_type: Optional[str] = Form(None),
        arabic: bool = Form(False),
        tone: str = Form("General"),
        current_user: SQLUser = Depends(fake_current_user),
        db: Session = Depends(get_db),
):
    logger.info(
        f"Analyze report endpoint hit. User ID: {current_user.id}, Service ID: {serviceId}, Blood Test ID: {testReportId}, Report Type: {report_type}, Arabic: {arabic}, Tone: {tone}",
        current_user, db)
    try:
        file_name = ""
        if reportFile:
            analysis_dict = report_analyzer(db, reportFile, arabic, tone, current_user, testReportId)
            logger.info(f"Email sent successfully to {current_user.email}.")
        elif testReportId:  # testReportId exist
            raise HTTPException(status_code=200, detail="Please provide a blood test ID.")  # for testing purpose only
        else:
            raise HTTPException(status_code=422, detail="Please provide either a report file or a blood test ID.")

        return analysis_dict  # AnalysisResult(**analysis_dict)

    except HTTPException as e:
        logger.error(f"HTTPException: {e} ")
        raise e
    except Exception as e:
        logger.error(f"Error processing analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing report analysis: {e}")
