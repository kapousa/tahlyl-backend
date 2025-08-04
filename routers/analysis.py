# analysis.py
from collections import defaultdict
from datetime import datetime
from typing import List, Optional, Dict, Any  # Ensure all types are imported

# *** Import Database correctly for type hinting if needed outside Depends ***
from pymongo.database import Database

# Import ALL dependencies from config explicitly
from config import get_mongo_db_sync, get_sqlite_db_sync

# Import core FastAPI components and types
from fastapi import APIRouter, HTTPException, File, Form, UploadFile, Depends, status  # Added status
from sqlalchemy.orm import Session  # For SQLAlchemy Session type

# Import your custom modules
from com.schemas.digitalProfile import DigitalProfile
from com.schemas.historicalMetric import MetricSummaryWithHistory
from com.services.programs import get_matching_programs
from com.services.report import \
    get_general_report_analysis_for_user  # Make sure this is correctly defined and returns AnalysisResult
from com.services.analysis import report_analyzer, deep_analyzer, get_historical_metric_values, fetch_user_metrics
from com.utils.AI import analyze_contents_by_gemini  # Assuming this is used elsewhere
from com.services.auth.jwt_security import get_current_user
from com.schemas.result import ResultCreate  # Assuming this is used elsewhere
from com.utils.Helper import extract_text_from_uploaded_report  # Assuming this is used elsewhere
from com.schemas.analysisResult import AnalysisResult  # Your Pydantic AnalysisResult model
from com.schemas.compareReports import CompareReports  # Assuming this is used elsewhere
from com.utils.Email import send_analysis_results_email, send_compare_report_email  # Assuming these are used elsewhere
from com.utils.Logger import logger
from com.utils.Report import save_report, save_analysis_result  # Assuming these are used elsewhere
from com.models.User import User as SQLUser  # Your SQLAlchemy User model

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/")
async def base_analysis():
    logger.info("Base analysis endpoint hit.")
    return {"Hello": "Analysis"}


@router.get("/digitalprofile", response_model=DigitalProfile)
def digital_profile_endpoint(current_user: SQLUser = Depends(get_current_user),
                             db: Session = Depends(get_sqlite_db_sync)):
    tone = "general"  # This 'tone' variable is not used in deep_analyzer's signature
    try:
        digital_profile = deep_analyzer(db, current_user.id, False)  # Removed 'tone' if deep_analyzer doesn't use it

        # Assuming deep_analyzer returns a dict that DigitalProfile can unpack
        return DigitalProfile(**digital_profile)

    except HTTPException as e:
        logger.error(f"Matric Summary HTTPException: {e.detail}")  # Use .detail for HTTPException
        raise e
    except Exception as e:
        logger.error(f"Error in digital profile: {e}", exc_info=True)  # Added exc_info
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error in digital profile: {e}")


@router.get("/metricssummary", response_model=Dict[str, MetricSummaryWithHistory])
def get_user_metrics_summary_and_history(current_user: SQLUser = Depends(get_current_user),
                                         db: Session = Depends(get_sqlite_db_sync)):
    """
    Retrieves the minimum of the last three available values and the last three
    individual values for key metrics for a specific user, structured by metric name.
    """
    try:
        all_user_metrics_data = fetch_user_metrics(db, current_user.id)

        transformed_metrics_summary = {}
        grouped_metrics = defaultdict(list)

        for metric_row in all_user_metrics_data:
            try:
                # Safely convert to float, handling potential None/non-numeric strings
                metric_row['metric_value_float'] = float(metric_row['metric_value']) if metric_row[
                                                                                            'metric_value'] is not None else None
            except (ValueError, TypeError):
                metric_row['metric_value_float'] = None

            grouped_metrics[metric_row['metric_name']].append(metric_row)

        for metric_name, metrics_list in grouped_metrics.items():
            # Ensure sort key exists, otherwise provide a fallback
            sorted_metrics = sorted(metrics_list,
                                    key=lambda x: x.get('report_added_datetime') or x.get(
                                        'result_added_datetime') or '',
                                    reverse=True)

            last_three_values = []
            for m in sorted_metrics[:3]:
                dt_value = m.get('report_added_datetime') or m.get('result_added_datetime')
                added_datetime_str = dt_value.isoformat() if isinstance(dt_value, datetime) else str(dt_value)

                last_three_values.append({
                    "value": str(m['metric_value']),
                    "added_datetime": added_datetime_str
                })

            numeric_values = [m['metric_value_float'] for m in sorted_metrics[:3] if
                              m['metric_value_float'] is not None]
            minimum_of_last_three = min(numeric_values) if numeric_values else None

            transformed_metrics_summary[metric_name] = MetricSummaryWithHistory(
                minimum_of_last_three=minimum_of_last_three,
                last_three_values=last_three_values
            )

        return transformed_metrics_summary

    except HTTPException as e:
        logger.error(f"Matric Summary HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error Matric Summary: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error processing Gemini response or saving report: {e}")


@router.post("/analyze", response_model=AnalysisResult)
def analyze_report_endpoint(
        serviceId: Optional[str] = Form(None),
        reportFile: Optional[UploadFile] = File(None),
        testReportId: Optional[str] = Form(None),
        report_type: Optional[str] = Form(None),
        arabic: bool = Form(False),
        tone: str = Form("General"),
        current_user: SQLUser = Depends(get_current_user),
        db: Session = Depends(get_sqlite_db_sync),  # Corrected: No ()
        mongo_db: Database = Depends(get_mongo_db_sync)  # Corrected: No ()
):
    logger.info(
        f"Analyze report endpoint hit. User ID: {current_user.id}, Service ID: {serviceId}, "
        f"Report File: {reportFile.filename if reportFile else 'N/A'}, Tone: {tone}, Arabic: {arabic}"
    )

    analysis_result_obj = None  # Will hold the Pydantic model instance

    try:
        if reportFile:
            # Assuming report_analyzer returns a dictionary that matches AnalysisResult's fields
            analysis_data_from_analyzer = report_analyzer(db, reportFile, arabic, tone, current_user, testReportId)
            # Create the Pydantic model instance
            analysis_result_obj = analysis_data_from_analyzer
            logger.info(f"Analysis generated from report file.")
        elif testReportId:
            analysis_result_obj = get_general_report_analysis_for_user(db, current_user.id, testReportId, tone)
            if not analysis_result_obj:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Analysis not found for provided testReportId and tone.")
            logger.info(f"Analysis retrieved for testReportId.")
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Please provide either a report file or a test report ID.")

        if not analysis_result_obj:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to generate or retrieve analysis.")

        matched_programs = get_matching_programs(mongo_db, analysis_result_obj)
        logger.info(f"Found {len(matched_programs)} matching programs for analysis.")

        # Modify the Pydantic model instance directly before returning
        # This requires `AnalysisResult` to have `matched_programs` as a field
        # and to be mutable (which Pydantic models are after instantiation).
        analysis_result_obj.matched_programs = matched_programs  # Assign the list of ProgramOffer objects

        # Return the Pydantic model instance. FastAPI will handle serialization.
        return analysis_result_obj

    except BaseException as e:
        logger.error(f"BaseException in analyze_report_endpoint: {e.detail}")
        raise e
    except HTTPException as e:
        logger.error(f"HTTPException in analyze_report_endpoint: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error processing analysis in analyze_report_endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error processing report analysis: {e}")