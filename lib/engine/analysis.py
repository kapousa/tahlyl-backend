import os
import re
import json
from typing import Optional

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user
from lib.models.User import User as SQLUser
from config import logger, get_db
from lib.constants import prompts
from lib.engine.security import get_current_user, fake_current_user
from lib.schemas.analysisResult import AnalysisResult
from lib.schemas.result import ResultCreate
from lib.utils.Email import send_analysis_results_email
from lib.utils.Helper import extract_text_from_pdf
from lib.utils.Report import save_analysis_result, save_report, detect_report_type
from lib.constants.prompts import (
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

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Ensure GOOGLE_API_KEY is in .env
model = genai.GenerativeModel('gemini-1.5-pro')
# model = genai.GenerativeModel('models/gemini-2.0-pro-exp')

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


def analyze_blood_test(blood_test_text: str, arabic: bool = False, tone: str = 'General'):
    tone = tone.lower()
    # if arabic:
    #     if tone == 'doctor':
    #         prompt = prompts.ARABIC_BLOOD_TEST_DOCTOR_PROMPT.format(blood_test_text=blood_test_text, tone=tone)
    #     elif tone == 'executive':
    #         prompt = prompts.ARABIC_BLOOD_TEST_EXECUTIVE_PROMPT.format(blood_test_text=blood_test_text, tone=tone)
    #     elif tone == 'educational':
    #         prompt = prompts.ARABIC_BLOOD_TEST_EDUCATIONAL_PROMPT.format(blood_test_text=blood_test_text, tone=tone)
    #     elif tone == 'preventative':
    #         prompt = prompts.ARABIC_BLOOD_TEST_PREVENTATIVE_PROMPT.format(blood_test_text=blood_test_text, tone=tone)
    #     elif tone == 'technical':
    #         prompt = prompts.ARABIC_BLOOD_TEST_TECHNICAL_PROMPT.format(blood_test_text=blood_test_text, tone=tone)
    #     elif tone == 'empathetic':
    #         prompt = prompts.ARABIC_BLOOD_TEST_EMPATHETIC_PROMPT.format(blood_test_text=blood_test_text, tone=tone)
    #     else:  # Default to General tone
    #         prompt = prompts.ARABIC_BLOOD_TEST_GENERAL_PROMPT.format(blood_test_text=blood_test_text, tone=tone)
    # else:
    #     if tone == 'doctor':
    #         prompt = prompts.ENGLISH_BLOOD_TEST_DOCTOR_PROMPT.format(blood_test_text=blood_test_text, tone=tone)
    #     elif tone == 'executive':
    #         prompt = prompts.ENGLISH_BLOOD_TEST_EXECUTIVE_PROMPT.format(blood_test_text=blood_test_text, tone=tone)
    #     elif tone == 'educational':
    #         prompt = prompts.ENGLISH_BLOOD_TEST_EDUCATIONAL_PROMPT.format(blood_test_text=blood_test_text)
    #     elif tone == 'preventative':
    #         prompt = prompts.ENGLISH_BLOOD_TEST_PREVENTATIVE_PROMPT.format(blood_test_text=blood_test_text, tone=tone)
    #     elif tone == 'technical':
    #         prompt = prompts.ENGLISH_BLOOD_TEST_TECHNICAL_PROMPT.format(blood_test_text=blood_test_text)
    #     elif tone == 'empathetic':
    #         prompt = prompts.ENGLISH_BLOOD_TEST_EMPATHETIC_PROMPT.format(blood_test_text=blood_test_text)
    #     else:  # Default to General tone
    #         prompt = prompts.ENGLISH_BLOOD_TEST_GENERAL_PROMPT.format(blood_test_text=blood_test_text)

    try:
        #response = model.generate_content(prompt)\
        response = model.generate_content(blood_test_text)
        if response.text:
            response_text = response.text

            # Remove the ```json and ``` that Gemini sometimes adds.
            response_text = response_text.replace("```json", "").replace("```", "").strip()

            try:
                analysis_json = json.loads(response_text)
                return analysis_json
            except json.JSONDecodeError as e:
                # Handle cases where Gemini's response is not valid JSON
                return {"error": f"Invalid JSON response from Gemini: {e}", "raw_response": response_text}
        else:
            return {"error": "There is no response text. This could be due to safety or copyright issues."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing blood test: {e}")


def compare_reports(reports: list[str], arabic: bool):
    """Compares blood test reports using Gemini with language option."""
    if arabic:
        prompt = f"""
        قارن بين تقارير اختبار الدم التالية وقدم ملخصًا موجزًا لتقدم حالة المريض في صيغة JSON.
        {{ "summary": "ملخص مقارنة التقارير..." }}

        {' '.join(reports)}
        """
    else:
        prompt = f"""
        Compare the following blood test reports and provide a brief summary of the patient's progress in JSON format.
        {{ "summary": "Summary of report comparison..." }}

        {' '.join(reports)}
        """
    try:
        response = model.generate_content(prompt)
        if response.text:
            response_text = response.text
            response_text = response_text.replace("```json", "").replace("```", "").strip()

            try:
                analysis_json = json.loads(response_text)
                return analysis_json
            except json.JSONDecodeError as e:
                # Improved JSON exception handling
                error_message = f"Invalid JSON response from Gemini: {e}. Raw response: {response_text}"
                print(error_message)  # Log error to console.
                return {"error": error_message, "raw_response": response_text}
        else:
            return {"error": "There is no response text. This could be due to safety or copyright issues."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing blood test: {e}")


def analyze_blood_test_trends_gemini(blood_test_reports_text):
    """Simulates trend analysis using Gemini."""
    prompt = f"""
    Analyze the following blood test reports to identify trends and potential future risks.
    Provide the analysis in JSON format, including:
    - "trends": A description of any observed trends in the blood test values.
    - "forecast": A brief prediction of potential future values or health risks based on the trends.

    Blood Test Reports:
    {blood_test_reports_text}

    JSON:
    """

    try:
        response = model.generate_content(prompt)
        if response.text:
            response_text = response.text
            response_text = response_text.replace("```json", "").replace("```", "").strip()

            try:
                analysis_json = json.loads(response_text)
                return analysis_json
            except json.JSONDecodeError as e:
                # Improved JSON exception handling
                error_message = f"Invalid JSON response from Gemini: {e}. Raw response: {response_text}"
                print(error_message)  # Log error to console.
                return {"error": error_message, "raw_response": response_text}
        else:
            return {"error": "There is no response text. This could be due to safety or copyright issues."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing blood test: {e}")


def get_supplement_recommendations_gemini(blood_test_results_text):
    """Simulates supplement recommendations using Gemini."""
    prompt = f"""
    Analyze the following blood test results to identify potential nutrient deficiencies and recommend appropriate supplements or dietary changes.
    Provide the recommendations in JSON format, including:
    - "deficiencies": A list of identified nutrient deficiencies.
    - "recommendations": A list of recommended supplements or dietary changes, including dosages.

    Blood Test Results:
    {blood_test_results_text}

    JSON:
    """
    try:
        response = model.generate_content(prompt)
        if response.text:
            response_text = response.text
            response_text = response_text.replace("```json", "").replace("```", "").strip()

            try:
                analysis_json = json.loads(response_text)
                return analysis_json
            except json.JSONDecodeError as e:
                # Improved JSON exception handling
                error_message = f"Invalid JSON response from Gemini: {e}. Raw response: {response_text}"
                print(error_message)  # Log error to console.
                return {"error": error_message, "raw_response": response_text}
        else:
            return {"error": "There is no response text. This could be due to safety or copyright issues."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing blood test: {e}")


def check_drug_interactions_gemini(medications_text, blood_test_results_text):
    """Simulates drug interaction checks using Gemini."""
    prompt = f"""
    Analyze the following list of medications and blood test results to identify potential drug interactions and medication effects.
    Provide the analysis in JSON format, including:
    - "interactions": A list of potential drug interactions.
    - "medication_effects": A description of the potential effects of the medications on the blood test results.

    Medications:
    {medications_text}

    Blood Test Results:
    {blood_test_results_text}

    JSON:
    """
    try:
        response = model.generate_content(prompt)
        if response.text:
            response_text = response.text
            response_text = response_text.replace("```json", "").replace("```", "").strip()

            try:
                analysis_json = json.loads(response_text)
                return analysis_json
            except json.JSONDecodeError as e:
                # Improved JSON exception handling
                error_message = f"Invalid JSON response from Gemini: {e}. Raw response: {response_text}"
                print(error_message)  # Log error to console.
                return {"error": error_message, "raw_response": response_text}
        else:
            return {"error": "There is no response text. This could be due to safety or copyright issues."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing blood test: {e}")


def get_lab_value_interpretation_gemini(lab_value_text, blood_test_results_text):
    """Simulates lab value interpretation using Gemini."""
    prompt = f"""
    Provide an interpretation of the following lab values based on the blood test results.
    Provide the interpretation in JSON format, including:
    - "interpretation": An explanation of the lab values and their significance.

    Lab Values:
    {lab_value_text}

    Blood Test Results:
    {blood_test_results_text}

    JSON:
    """
    try:
        response = model.generate_content(prompt)
        if response.text:
            response_text = response.text
            response_text = response_text.replace("```json", "").replace("```", "").strip()

            try:
                analysis_json = json.loads(response_text)
                return analysis_json
            except json.JSONDecodeError as e:
                # Improved JSON exception handling
                error_message = f"Invalid JSON response from Gemini: {e}. Raw response: {response_text}"
                print(error_message)  # Log error to console.
                return {"error": error_message, "raw_response": response_text}
        else:
            return {"error": "There is no response text. This could be due to safety or copyright issues."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing blood test: {e}")


def reportAnalyzer(
        report_file,
        report_type,
        arabic,
        tone: str,
        current_user,
        db: Session,
):
    print(current_user)
    tone = tone.lower()
    language = "ar" if arabic else "en"

    try:
        medical_test_text = extract_text_from_pdf(report_file)
        detected_report_type = report_type
        if report_type == "unknown":
            detected_report_type = detect_report_type(medical_test_text)
            logger.info(f"Detected report type: {detected_report_type}")
            if not detected_report_type:
                logger.warning("Could not automatically detect report type. Using general prompt.")
                prompt = REPORT_TYPE_PROMPT_MAP.get("general", {"en": ENGLISH_BLOOD_TEST_GENERAL_PROMPT,
                                                                "ar": ARABIC_BLOOD_TEST_GENERAL_PROMPT}).get(language)
            else:
                prompt = REPORT_TYPE_PROMPT_MAP.get(detected_report_type, {"en": ENGLISH_BLOOD_TEST_GENERAL_PROMPT,
                                                                           "ar": ARABIC_BLOOD_TEST_GENERAL_PROMPT}).get(
                    language)
        elif report_type:
            prompt = REPORT_TYPE_PROMPT_MAP.get(report_type, {"en": ENGLISH_BLOOD_TEST_GENERAL_PROMPT,
                                                              "ar": ARABIC_BLOOD_TEST_GENERAL_PROMPT}).get(language)
        else:
            logger.warning("No report type specified. Using general prompt.")
            prompt = REPORT_TYPE_PROMPT_MAP.get("general", {"en": ENGLISH_BLOOD_TEST_GENERAL_PROMPT,
                                                            "ar": ARABIC_BLOOD_TEST_GENERAL_PROMPT}).get(language)

        if not prompt:
            logger.error(f"No prompt found for report type: {detected_report_type} and language: {language}")
            raise HTTPException(status_code=500, detail="Error: Could not find the appropriate analysis prompt.")

        formatted_prompt = prompt.format(blood_test_text=medical_test_text, tone=tone)
        logger.info(f"Using prompt: {formatted_prompt[:150]}...")  # Log first 150 chars of prompt

        analysis_dict = analyze_blood_test(prompt, arabic, tone)  # Call Gemini

        # Save the report
        # report_data = {
        #     "name": report_file.filename,
        #     "content": "medical_test_text",
        #     "location": "location",
        #     "user_id": current_user.id
        # }
        # report = save_report(report_data, current_user.id, db)
        # logger.info(f"Report saved to database with ID: {report.id} for user: {current_user.id}")

        # Save the analysis result
        # result_data = ResultCreate(
        #     result=analysis_dict.get("interpretation", "Analysis Result"),  # Adjust based on your Gemini output
        #     report_id=report.id,
        #     tone_id=tone,  # Assuming 'tone' string is what you want to save
        # )
        # saved_result = save_analysis_result(result_data, db)
        # logger.info(f"Analysis result saved to database with ID: {saved_result.id} for report: {report.id}")


        send_analysis_results_email(current_user.email, analysis_dict, arabic)

        return AnalysisResult(**analysis_dict)

    except HTTPException as e:
        logger.error(f"HTTPException: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error processing Gemini response or saving report: {e.with_traceback()}")
        raise HTTPException(status_code=500, detail=f"Error processing report analysis: {e}")
