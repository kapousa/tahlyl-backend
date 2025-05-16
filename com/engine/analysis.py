import json

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from config import logger, get_db
from com.curds.Metric import create_metrics
from com.engine.security import get_current_user
from com.schemas.analysisResult import AnalysisResult
from com.utils import Helper
from com.utils.AI import analyze_report_by_gemini
from com.utils.Email import send_analysis_results_email
from com.utils.Report import save_report, detect_report_type, save_analysis_result
from com.schemas.result import ResultCreate
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


@app.post("/analyze_report/")  # Example route, adjust as needed
async def analyze_report_endpoint(
        medical_test_content: str,
        arabic: bool,
        tone: str,
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db),
        file_name: str = ""  # Added file_name here
):
    """Example route to call report_analyzer"""
    try:
        analysis_result = report_analyzer(medical_test_content, arabic, tone, current_user, file_name, db)
        return analysis_result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing report: {e}")


def report_analyzer(db: Session,
                    medical_test_content: str,
                    arabic: bool,
                    tone: str,
                    current_user: dict,  # Assuming current_user is a dict here
                    file_name: str,
                    report_id: str = ""):
    tone = tone.lower()
    language = "ar" if arabic else "en"

    try:
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

        analysis_dict = analyze_report_by_gemini(formatted_prompt)  # Call Gemini
        # logger.info(f"Gemini Analysis Dictionary: {analysis_dict}")  # <--- ADD THIS LINE

        # Save the report
        report_data = {
            "id": Helper.generate_id(),
            "name": file_name,
            "content": medical_test_content,
            "location": "location",
            "user_id": current_user.id  # Access user_id as dict
        }
        report = save_report(report_data, db)  # Pass db explicitly

        # Save the analysis result
        result_data = {  # Use ResultCreate schema
            "result": json.dumps(analysis_dict, ensure_ascii=False),  # retrieve as analysis_dict = json.loads(result)
            "report_id": report.id,
            "tone_id": tone,  # Assuming 'tone' string is what you want to save
            "language": language
        }
        saved_result = save_analysis_result(result_data, db)

        # Send email with the analysis results
        send_analysis_results_email(detected_report_type, current_user.email, analysis_dict,
                                    arabic)  # <--- STILL USING DICT ACCESS

        return AnalysisResult(**analysis_dict)

    except HTTPException as e:
        logger.error(f"HTTPException: {e.args[0]}")
        raise HTTPException(status_code=500, detail=f"Error processing report analysis: {e}")
    except Exception as e:
        logger.error(f"Error processing Gemini response or saving report: {e.args[0]}")
        raise HTTPException(status_code=500, detail=f"Error processing report analysis: {e}")
