import inspect
import json
from datetime import datetime
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from sqlalchemy import Column, desc, text
from sqlalchemy.orm import Session

from com.constants.deep_analysis_prompts import ARABIC_DIGITAL_PROFILE_PROMPT, ENGLISH_DIGITAL_PROFILE_PROMPT
from com.services.digitalProfile import create_digital_profile
from com.services.smartFeatures import analyze_health_trends
from com.schemas.digitalProfile import DigitalProfile
from com.schemas.historicalMetric import historicalMetric, MetricSummaryWithHistory
from com.utils.Logger import logger
from com.utils.Helper import extract_text_from_uploaded_report
from config import logger
from com.models.Report import Report as SQLReport
from com.models.Result import Result as SQLResult
from com.schemas.analysisResult import AnalysisResult
from com.utils import Helper
from com.utils.AI import analyze_contents_by_gemini
from com.utils.Email import send_analysis_results_email
from com.utils.Report import save_report, detect_report_type, save_analysis_result
from com.constants.prompts import (
    ENGLISH_CBC_PROMPT, ARABIC_CBC_PROMPT,
    ENGLISH_COMPARE_PROMPT, ARABIC_COMPARE_PROMPT,
    ENGLISH_GLUCOSE_PROMPT, ARABIC_GLUCOSE_PROMPT,
    ENGLISH_LIVER_PROMPT, ARABIC_LIVER_PROMPT,
    ENGLISH_KIDNEY_PROMPT, ARABIC_KIDNEY_PROMPT,
    ENGLISH_LIPID_PROMPT, ARABIC_LIPID_PROMPT,
    ENGLISH_HBA1C_PROMPT, ARABIC_HBA1C_PROMPT,
    ENGLISH_VITAMIN_D_PROMPT, ARABIC_VITAMIN_D_PROMPT,
    ENGLISH_THYROID_PROMPT, ARABIC_THYROID_PROMPT,
    ENGLISH_IRON_PROMPT, ARABIC_IRON_PROMPT,
    ENGLISH_INFLAMMATION_PROMPT, ARABIC_INFLAMMATION_PROMPT,
    ENGLISH_BLOOD_TEST_GENERAL_PROMPT, ARABIC_BLOOD_TEST_GENERAL_PROMPT,  # Fallback
)

load_dotenv()

app = FastAPI()

REPORT_TYPE_PROMPT_MAP = {
    "cbc": {"en": ENGLISH_CBC_PROMPT, "ar": ARABIC_CBC_PROMPT},
    "compare": {"en": ENGLISH_COMPARE_PROMPT, "ar": ARABIC_COMPARE_PROMPT},
    "glucose": {"en": ENGLISH_GLUCOSE_PROMPT, "ar": ARABIC_GLUCOSE_PROMPT},
    "liver": {"en": ENGLISH_LIVER_PROMPT, "ar": ARABIC_LIVER_PROMPT},
    "kidney": {"en": ENGLISH_KIDNEY_PROMPT, "ar": ARABIC_KIDNEY_PROMPT},
    "lipid": {"en": ENGLISH_LIPID_PROMPT, "ar": ARABIC_LIPID_PROMPT},
    "hba1c": {"en": ENGLISH_HBA1C_PROMPT, "ar": ARABIC_HBA1C_PROMPT},
    "vitamin_d": {"en": ENGLISH_VITAMIN_D_PROMPT, "ar": ARABIC_VITAMIN_D_PROMPT},
    "thyroid": {"en": ENGLISH_THYROID_PROMPT, "ar": ARABIC_THYROID_PROMPT},
    "iron": {"en": ENGLISH_IRON_PROMPT, "ar": ARABIC_IRON_PROMPT},
    "inflammation": {"en": ENGLISH_INFLAMMATION_PROMPT, "ar": ARABIC_INFLAMMATION_PROMPT},
}


def report_analyzer(db: Session,
                    reportFile,
                    arabic: bool,
                    tone: str,
                    current_user: dict,  # Assuming current_user is a dict here
                    background_tasks: BackgroundTasks,
                    report_id: str = ""):
    tone = tone.lower()
    language = "ar" if arabic else "en"

    try:
        file_name = reportFile.filename
        medical_test_content = extract_text_from_uploaded_report(reportFile)

        # check if the report and results with required tone and language are exist
        db_report = db.query(SQLReport).filter(SQLReport.content == medical_test_content).first()
        db_result = None
        if db_report is not None:
            db_result = db.query(SQLResult).filter(SQLResult.report_id == db_report.id,
                                                   SQLResult.tone_id == tone, SQLResult.language).first()

        if db_report is None or (
                db_report is not None and db_result is None):  # New report of exist report but request results with new tone
            detected_report_type = detect_report_type(medical_test_content)
            logger.info(f"Detected report type: {detected_report_type}")
            if not detected_report_type:
                logger.warning("Could not automatically detect report type. Using general prompt.")
                prompt = REPORT_TYPE_PROMPT_MAP.get("general", {"en": ENGLISH_BLOOD_TEST_GENERAL_PROMPT,
                                                                "ar": ARABIC_BLOOD_TEST_GENERAL_PROMPT}).get(language)
            else:
                prompt = REPORT_TYPE_PROMPT_MAP.get(detected_report_type, {"en": ENGLISH_BLOOD_TEST_GENERAL_PROMPT,
                                                                           "ar": ARABIC_BLOOD_TEST_GENERAL_PROMPT}).get(
                    language)
            if not prompt:
                logger.error(f"No prompt found for report type: {detected_report_type} and language: {language}")
                raise HTTPException(status_code=500, detail="Error: Could not find the appropriate analysis prompt.")

            formatted_prompt = prompt.format(blood_test_text=medical_test_content, tone=tone)
            logger.info(f"Using prompt: {formatted_prompt[:150]}...")  # Log first 150 chars of prompt

            analysis_dict = analyze_contents_by_gemini(formatted_prompt)  # Call Gemini
            # logger.info(f"Gemini Analysis Dictionary: {analysis_dict}")  # <--- ADD THIS LINE

            report_id = Helper.generate_id() if db_report is None else db_report.id
            if db_report is None:
                # Save the report
                report_data = {
                    "id": report_id,
                    "name": file_name,
                    "content": medical_test_content,
                    "report_type": detected_report_type,
                    "status": "normal",
                    "location": "location",
                    "user_id": current_user.id  # Access user_id as dict
                }
                report = save_report(report_data, db)  # Pass db explicitly

            if db_result is None:
                # Save the analysis result
                result_data = {  # Use ResultCreate schema
                    "result": json.dumps(analysis_dict, ensure_ascii=False),
                    # retrieve as analysis_dict = json.loads(result)
                    "report_id": report_id,
                    "tone_id": tone,  # Assuming 'tone' string is what you want to save
                    "language": language
                }
                saved_result = save_analysis_result(result_data, db)


        else:  # Results of required report and tone exist
            detected_report_type = db_report.report_type
            analysis_dict = json.loads(db_result.result)

        # Send email with the analysis results
        send_analysis_results_email(detected_report_type, current_user.email, analysis_dict, arabic)

        update_digital_profile= deep_analyzer(db, current_user.id, arabic)

        return AnalysisResult(**analysis_dict)

    except HTTPException as e:
        func_name = inspect.currentframe().f_code.co_name
        logger.error(f"Error processing report analysis '{func_name}': {e}")
        raise HTTPException(status_code=500, detail=f"Error processing report analysis '{func_name}': {e}")
    except Exception as e:
        func_name = inspect.currentframe().f_code.co_name
        logger.error(f"Error processing Gemini response or saving report '{func_name}': {e}")
        raise HTTPException(status_code=500,
                            detail=f"Error processing Gemini response or saving report '{func_name}': {e}")


def deep_analyzer(db: Session, user_id: str, arabic: bool):
    """
    Process deep analysis using all user's reports and generate information of the user's digital profile
    :param user_id:
    :param arabic:
    :param tone:
    :return: user's digital profile
    """
    # db: Session = SessionLocal()  # <--- IMPORTANT: Get a NEW session for the background task
    try:
        analysis_collection: List[SQLResult] = db.query(SQLResult).join(SQLResult.report).filter(
            SQLReport.user_id == user_id).all()

        results_strings = []
        for result in analysis_collection:
            try:
                analysis_content = json.loads(result.result)
            except json.JSONDecodeError:
                analysis_content = {"error": "Invalid JSON in result.result"}

            result_info = (
                f"report_id: {result.report_id}, "
                f"tone: {result.tone_id}, "
                f"language: {result.language}, "
                f"summary: {analysis_content.get('summary', 'N/A')}, "
                f"recommendations: {analysis_content.get('recommendations', 'N/A')}"
            )
            if result.report:
                report_info = (
                    f" (Result ID: {result.id}, "
                    f"Report Name: {result.report.name}, "
                    f"Date: {result.report.added_datetime})"
                )
                result_info += report_info

            results_strings.append(result_info)

        health_results_text = ", ".join(results_strings)

        if not health_results_text:
            logger.warning(f"No analysis results found for user {user_id} for deep analysis.")
            empty_profile_data = {
                "health_overview": "No analysis data available to generate a comprehensive profile.",
                "recommendations": [],  # Keep as list
                "attention_points": [],  # Keep as list
                "risks": [],  # Keep as list
                "creation_date": datetime.utcnow().isoformat(),
                "recent": 1,
                "user_id": user_id,
                "id": Helper.generate_id()
            }
            digital_profile_schema_obj = DigitalProfile(**empty_profile_data)
            create_digital_profile(digital_profile_schema_obj, db)
            return empty_profile_data  # Return the dict directly, FastAPI will serialize it

        if arabic:
            prompt = ARABIC_DIGITAL_PROFILE_PROMPT.format(health_results_text=health_results_text)
        else:
            prompt = ENGLISH_DIGITAL_PROFILE_PROMPT.format(health_results_text=health_results_text)

        digital_profile_dict = analyze_contents_by_gemini(prompt)

        final_digital_profile_data = {
            "id": Helper.generate_id(),
            "user_id": user_id,
            "health_overview": digital_profile_dict.get("overview_health_status", ""),
            "recommendations": digital_profile_dict.get("recommendations", []),
            "attention_points": digital_profile_dict.get("attention_points", []),
            "risks": digital_profile_dict.get("risks", []),
            "creation_date": datetime.utcnow().isoformat(),
            "recent": 1
        }


        digital_profile_schema_obj = DigitalProfile(**final_digital_profile_data)
        created_dp = create_digital_profile(digital_profile_schema_obj, db)

        # Fetch metrics history
        metrics_history = fetch_user_metrics(db, user_id)
        final_digital_profile_data['metrics'] = metrics_history

        # Log the dictionary using logger, not print
        logger.info(f"Final Digital Profile Data: {json.dumps(final_digital_profile_data, indent=2)}")

        return final_digital_profile_data

    except Exception as e:
        func_name = inspect.currentframe().f_code.co_name
        logger.error(f"Deep analysis exception in '{func_name}': {e}", exc_info=True)
        raise

def fetch_user_metrics(db: Session, user_id):
    """
    Retrieves all metric values from the last three report results for a given user.

    Args:
        db: The SQLAlchemy database session.
        user_id: The ID of the user whose reports to query.

    Returns:
        A list of dictionaries, where each dictionary represents a metric
        and includes associated result and report information.
    """
    sql_query = text(f"""
        WITH LastThreeReports AS (
            SELECT
                id AS report_id,
                added_datetime
            FROM
                report
            WHERE
                user_id = :user_id
            ORDER BY
                added_datetime DESC
            LIMIT 3
        )
        SELECT
            m.id AS metric_id,
            m.name AS metric_name,
            m.value AS metric_value,
            m.unit AS metric_unit,
            m.reference_range_min,
            m.reference_range_max,
            m.status AS metric_status,
            r.id AS result_id,
            r.tone_id,
            r.added_datetime AS result_added_datetime,
            r.language,
            l3r.report_id,
            l3r.added_datetime AS report_added_datetime,
            rep.name AS report_name
        FROM
            metric m
        JOIN
            result r ON m.result_id = r.id
        JOIN
            report rep ON r.report_id = rep.id
        JOIN
            LastThreeReports l3r ON rep.id = l3r.report_id
        ORDER BY
            l3r.added_datetime DESC,
            r.added_datetime DESC,
            m.name;
    """)
    results = db.execute(sql_query, {"user_id": user_id}).mappings().all()
    list_of_dicts = [dict(row) for row in results]

    # TODO
    # will remove comment sign when enable smart services
    # Get health trends
    # health_trends= analyze_health_trends(list_of_dicts)

    return list_of_dicts

def get_historical_metric_values(db: Session, user_id: str, metric_column: Column, n: int = 1) -> List[historicalMetric]:
    results = db.query(
        metric_column,
        SQLResult.added_datetime
    ).filter(
        SQLResult.report.has(user_id=user_id),
        metric_column.isnot(None)
    ).order_by(
        desc(SQLResult.added_datetime)
    ).limit(n).all()
    return [historicalMetric(value=r[0], added_datetime=r[1]) for r in results if r[0] is not None]


