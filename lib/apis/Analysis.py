import os
import io
import google.generativeai as genai
from pdfminer.high_level import extract_text  # Correct import
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, HTTPException

load_dotenv()

app = FastAPI()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Ensure GOOGLE_API_KEY is in .env
model = genai.GenerativeModel('models/gemini-2.0-pro-exp')

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

import json
from fastapi import HTTPException

def analyze_blood_test(blood_test_text: str, arabic: bool = False):
    if arabic:
        prompt = f"""
                حلل نتائج اختبار الدم التالية وقدم باللغة العربية استجابة بتنسيق JSON.
                يجب أن يحتوي JSON على المفاتيح التالية:
                - "summary": ملخص موجز لنتائج اختبار الدم.
                - "lifestyle_changes": قائمة بالتغييرات المقترحة في نمط الحياة لتحسين النتائج.
                - "diet_routine": قائمة بالتوصيات الغذائية بناءً على النتائج.

                نتائج اختبار الدم:
                {blood_test_text}

                JSON:
                """
    else:
        prompt = f"""
            Analyze the following blood test results and provide a response in JSON format.
            The JSON should contain the following keys:
            - "summary": A concise summary of the blood test results.
            - "lifestyle_changes": A list of suggested lifestyle changes to improve the results.
            - "diet_routine": A list of dietary recommendations based on the results.

            Blood test results:
            {blood_test_text}

            JSON:
            """
    try:
        response = model.generate_content(prompt)
        response_text = response.text

        # Remove the ```json and ``` that Gemini sometimes adds.
        response_text = response_text.replace("```json", "").replace("```", "").strip()

        try:
            analysis_json = json.loads(response_text)
            return analysis_json
        except json.JSONDecodeError as e:
            # Handle cases where Gemini's response is not valid JSON
            return {"error": f"Invalid JSON response from Gemini: {e}", "raw_response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing blood test: {e}")

# Example endpoint (you'll need to create a route for file upload and analysis)
# @app.post("/analyze_pdf/")
# async def analyze_pdf(pdf_file: UploadFile):
#     try:
#         pdf_text = extract_text_from_pdf(pdf_file)
#         analysis = analyze_blood_test(pdf_text)
#         return {"analysis": analysis}
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")