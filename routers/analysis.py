# analysis.py
from collections import defaultdict
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, File, Form, UploadFile, Depends
from pdfminer.high_level import extract_text
from sqlalchemy.orm import Session
from typing import Dict
from com.schemas.digitalProfile import DigitalProfile
from com.schemas.historicalMetric import MetricSummaryWithHistory
from config import get_db
from com.engine.analysis import report_analyzer, deep_analyzer, get_historical_metric_values, fetch_user_metrics
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
def digital_profile_endpoint(current_user: SQLUser = Depends(get_current_user), db: Session = Depends(get_db)):
    tone = "general"
    try:
        digital_profile = deep_analyzer(db, current_user.id, False, tone)

        return DigitalProfile(**digital_profile)

    except HTTPException as e:
        logger.error(f"HTTPException: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error processing Gemini response or saving report: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing Gemini response or saving report: {e}")

@router.get("/metricssummary", response_model=Dict[str, MetricSummaryWithHistory])  # <--- Change here
def get_user_metrics_summary_and_history(current_user: SQLUser = Depends(get_current_user),
                                         db: Session = Depends(get_db)):
    """
    Retrieves the minimum of the last three available values and the last three
    individual values for key metrics for a specific user, structured by metric name.
    """
    all_user_metrics_data = fetch_user_metrics(db, current_user.id)  # This returns List[Dict]

    transformed_metrics_summary = {}  # This will be the dict we return
    grouped_metrics = defaultdict(list)

    for metric_row in all_user_metrics_data:
        try:
            metric_row['metric_value_float'] = float(metric_row['metric_value'])
        except (ValueError, TypeError):
            metric_row['metric_value_float'] = None

        grouped_metrics[metric_row['metric_name']].append(metric_row)

    for metric_name, metrics_list in grouped_metrics.items():
        sorted_metrics = sorted(metrics_list,
                                key=lambda x: x.get('report_added_datetime') or x.get('result_added_datetime', ''),
                                reverse=True)

        last_three_values = []
        for m in sorted_metrics[:3]:
            dt_value = m.get('report_added_datetime') or m.get('result_added_datetime')
            added_datetime_str = dt_value.isoformat() if isinstance(dt_value, datetime) else str(dt_value)

            last_three_values.append({
                "value": str(m['metric_value']),
                "added_datetime": added_datetime_str
            })

        numeric_values = [m['metric_value_float'] for m in sorted_metrics[:3] if m['metric_value_float'] is not None]
        minimum_of_last_three = min(numeric_values) if numeric_values else None

        transformed_metrics_summary[metric_name] = MetricSummaryWithHistory(
            minimum_of_last_three=minimum_of_last_three,
            last_three_values=last_three_values
        )

    return transformed_metrics_summary

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
def analyze_report_endpoint(
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
        f"Analyze report endpoint hit. User ID: {current_user.id}, Service ID: {serviceId}, "
        f"Blood Test ID: {testReportId}, Report Type: {report_type}, Arabic: {arabic}, Tone: {tone}"
    )
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
