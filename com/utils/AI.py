import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def analyze_report_by_gemini(blood_test_text: str):
    try:
        # Configure Gemini API
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)  # Ensure GOOGLE_API_KEY is in .env
        model = genai.GenerativeModel('gemini-1.5-flash')

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
                raise {"error": f"Invalid JSON response from Gemini: {e}", "raw_response": response_text}
        else:
            raise {"Error": "There is no response text. This could be due to safety or copyright issues."}

    except Exception as e:
        raise {"Error": e.args[0]}
