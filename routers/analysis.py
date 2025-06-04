# analysis.py
from typing import List, Optional

from fastapi import APIRouter, HTTPException, File, Form, UploadFile, Depends
from pdfminer.high_level import extract_text
from sqlalchemy.orm import Session

from com.schemas.digitalProfile import DigitalProfile
from config import get_db
from com.engine.analysis import report_analyzer, deep_analyzer
from com.utils.AI import analyze_contents_by_gemini
from com.engine.auth.jwt_security import get_current_user
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


@router.post("/digitalprofile", response_model=DigitalProfile)
async def digital_profile_endpoint(current_user: SQLUser = Depends(get_current_user), db: Session = Depends(get_db)):
    tone = "general"
    try:
        digital_profile = deep_analyzer(db, current_user.id, tone)

        return digital_profile  #DigitalProfile(**digital_profile)

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
        current_user: SQLUser = Depends(get_current_user),
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
