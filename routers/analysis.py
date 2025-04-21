# analysis.py
import os
from typing import List, Union

from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from pdfminer.high_level import extract_text

from lib.libs.Analysis import analyze_blood_test, compare_reports, model
from lib.utils.Helper import extract_text_from_pdf
from lib.schemas.AnalysisResult import AnalysisResult
from lib.schemas.CompareReports import CompareReports
from lib.utils.Email import send_analysis_results_email, send_compare_report_email
from lib.utils.Logger import logger
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
        response_text = response.text
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        return json.loads(response_text)
    except Exception as e:
        return {"error": f"Error analyzing trends: {e}"}

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
        response_text = response.text
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        return json.loads(response_text)
    except Exception as e:
        return {"error": f"Error getting supplement recommendations: {e}"}

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
        response_text = response.text
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        return json.loads(response_text)
    except Exception as e:
        return {"error": f"Error checking drug interactions: {e}"}

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
        response_text = response.text
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        return json.loads(response_text)
    except Exception as e:
        return {"error": f"Error getting lab value interpretation: {e}"}

@router.post("/analyze_trends")
async def analyze_trends(pdf_file: UploadFile = File(...)):
    blood_test_text = extract_text_from_pdf(pdf_file)
    return analyze_blood_test_trends_gemini(blood_test_text)

@router.post("/supplement_recommendations")
async def supplement_recommendations(pdf_file: UploadFile = File(...)):
    blood_test_text = extract_text_from_pdf(pdf_file)
    return get_supplement_recommendations_gemini(blood_test_text)

@router.post("/drug_interactions")
async def drug_interactions(pdf_file: UploadFile = File(...), medications: str = Form(...)):
    blood_test_text = extract_text_from_pdf(pdf_file)
    return check_drug_interactions_gemini(medications, blood_test_text)

@router.post("/lab_interpretation")
async def lab_interpretation(pdf_file: UploadFile = File(...), lab_values: str = Form(...)):
    blood_test_text = extract_text_from_pdf(pdf_file)
    return get_lab_value_interpretation_gemini(lab_values, blood_test_text)