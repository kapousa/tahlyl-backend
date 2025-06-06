import inspect
import json
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from com.constants.deep_analysis_prompts import ARABIC_DIGITAL_PROFILE_PROMPT, ENGLISH_DIGITAL_PROFILE_PROMPT
from com.schemas.digitalProfile import DigitalProfile
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
                    report_id: str = ""):
    tone = tone.lower()
    language = "ar" if arabic else "en"

    try:
        file_name = reportFile.filename
        medical_test_content = extract_text_from_uploaded_report(reportFile)

        # check if the report and results with required tone are exist
        db_report = db.query(SQLReport).filter(SQLReport.content == medical_test_content).first()
        db_result = None
        if db_report is not None:
            db_result = db.query(SQLResult).filter(SQLResult.report_id == db_report.id,
                                                   SQLResult.tone_id == tone).first()

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


def deep_analyzer(db: Session, user_id: str, arabic: bool = False, tone: str = "general"):
    """
    Process deep analysis using all user's reports and generate information of the user's digital profile
    :param user_id:
    :return: user's digital profile
    """
    try:
        # 1. Fetch the analysis results
        analysis_collection: List[SQLResult] = db.query(SQLResult).join(SQLResult.report).filter(
            SQLReport.user_id == user_id).all()

        # 2. Extract relevant data and format it
        results_strings = []
        for result in analysis_collection:
            result_info = (
                f"analysis_result: {result.result}, "
            )
            # You might also want to include the report details if relevant
            if result.report:
                report_info = (
                    f" (Result ID: {result.id}, "
                    f"Date: {result.report.added_datetime})"
                )
                result_info += report_info

            results_strings.append(result_info)

        # 3. Join the formatted strings into a single comma-separated string
        health_results_text = ", ".join(results_strings)

        if arabic:
            prompt = ARABIC_DIGITAL_PROFILE_PROMPT.format(health_results_text=health_results_text)
        else:
            prompt = ENGLISH_DIGITAL_PROFILE_PROMPT.format(health_results_text=health_results_text)

        digital_profile_dict = analyze_contents_by_gemini(prompt)

        return DigitalProfile(**digital_profile_dict)

    except Exception as e:
        func_name = inspect.currentframe().f_code.co_name
        logger.error(f"Deep analysis exception in '{func_name}': {e}")
        raise HTTPException(status_code=500, detail=f"Deep analysis exception in '{func_name}': {e}")
