import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from lib.constants import prompts

load_dotenv()

app = FastAPI()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Ensure GOOGLE_API_KEY is in .env
model = genai.GenerativeModel('gemini-1.5-pro')
#model = genai.GenerativeModel('models/gemini-2.0-pro-exp')


def analyze_blood_test(blood_test_text: str, arabic: bool = False, tone : str = 'General' ):
    tone = tone.lower()
    if arabic:
        if tone == 'doctor':
            prompt = prompts.ARABIC_BLOOD_TEST_DOCTOR_PROMPT.format(blood_test_text=blood_test_text)
        elif tone == 'executive':
            prompt = prompts.ARABIC_BLOOD_TEST_EXECUTIVE_PROMPT.format(blood_test_text=blood_test_text)
        elif tone == 'educational':
            prompt = prompts.ARABIC_BLOOD_TEST_EDUCATIONAL_PROMPT.format(blood_test_text=blood_test_text)
        elif tone == 'preventative':
            prompt = prompts.ARABIC_BLOOD_TEST_PREVENTATIVE_PROMPT.format(blood_test_text=blood_test_text)
        elif tone == 'technical':
            prompt = prompts.ARABIC_BLOOD_TEST_TECHNICAL_PROMPT.format(blood_test_text=blood_test_text)
        elif tone == 'empathetic':
            prompt = prompts.ARABIC_BLOOD_TEST_EMPATHETIC_PROMPT.format(blood_test_text=blood_test_text)
        else:  # Default to General tone
            prompt = prompts.ARABIC_BLOOD_TEST_GENERAL_PROMPT.format(blood_test_text=blood_test_text)
    else:
        if tone == 'doctor':
            prompt = prompts.ENGLISH_BLOOD_TEST_DOCTOR_PROMPT.format(blood_test_text=blood_test_text)
        elif tone == 'executive':
            prompt = prompts.ENGLISH_BLOOD_TEST_EXECUTIVE_PROMPT.format(blood_test_text=blood_test_text)
        elif tone == 'educational':
            prompt = prompts.ENGLISH_BLOOD_TEST_EDUCATIONAL_PROMPT.format(blood_test_text=blood_test_text)
        elif tone == 'preventative':
            prompt = prompts.ENGLISH_BLOOD_TEST_PREVENTATIVE_PROMPT.format(blood_test_text=blood_test_text)
        elif tone == 'technical':
            prompt = prompts.ENGLISH_BLOOD_TEST_TECHNICAL_PROMPT.format(blood_test_text=blood_test_text)
        elif tone == 'empathetic':
            prompt = prompts.ENGLISH_BLOOD_TEST_EMPATHETIC_PROMPT.format(blood_test_text=blood_test_text)
        else:  # Default to General tone
            prompt = prompts.ENGLISH_BLOOD_TEST_GENERAL_PROMPT.format(blood_test_text=blood_test_text)

    try:
        response = model.generate_content(prompt)
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

