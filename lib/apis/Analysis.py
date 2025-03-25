import os
import io
from typing import List
import re
import json
import google.generativeai as genai
from pdfminer.high_level import extract_text  # Correct import
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, HTTPException

from lib.constants import prompts

load_dotenv()

app = FastAPI()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Ensure GOOGLE_API_KEY is in .env
model = genai.GenerativeModel('models/gemini-1.5-pro')
#model = genai.GenerativeModel('models/gemini-2.0-pro-exp')
# for model in genai.list_models():
#     print(model)

def extract_text_from_pdf(pdf_file: UploadFile):
    """Extracts text from a PDF file."""
    try:
        pdf_content = pdf_file.file.read()
        text_io = io.BytesIO(pdf_content)
        text = extract_text(text_io)  # Corrected Line
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from PDF: {e}")

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
        print(f"Gemini Response: {response.text!r}")

        # Check for empty response
        if not response.text.strip():
            raise ValueError("Gemini returned an empty response.")

        # Attempt to find JSON pattern
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)

        if json_match:
            try:
                response_dict = json.loads(json_match.group(0))
                summary = response_dict.get("summary", "")  # get the summary or empty string if it does not exist.

                # Convert newlines to <br> tags
                summary_html = summary.replace('\n', '<br>')

                # Convert Markdown bold to <strong> tags
                summary_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', summary_html)

                # Convert Markdown bold to <li> tags
                summary_html = re.sub(r'\*(.*?)\*', r'<li>\1</li>', summary_html)

                response_dict["summary"] = summary_html  # update the dictionary with the html summary.

                return response_dict
            except json.JSONDecodeError as e:
                # Log the raw response for debugging
                print(f"JSONDecodeError: {e}. Raw response: {response.text!r}")
                raise ValueError(f"Gemini did not return valid JSON: {e}")
        else:
            # Log the raw response for debugging
            print(f"Gemini did not return JSON. Raw response: {response.text!r}")
            raise ValueError("Gemini did not return JSON.")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

