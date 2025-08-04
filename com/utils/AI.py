import inspect
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

from com.utils.Logger import logger
from com.utils.Helper import extract_text_from_uploaded_report
from config import logger

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
generative_model= 'gemini-1.5-flash'

def analyze_contents_by_gemini(blood_test_text: str):
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)  # Ensure GOOGLE_API_KEY is in .env
        model = genai.GenerativeModel(generative_model)

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
                func_name = inspect.currentframe().f_code.co_name
                raise {"error": f"func name: {func_name}: Invalid JSON response from Gemini: {e}", "raw_response": response_text}
        else:
            func_name = inspect.currentframe().f_code.co_name
            raise {"Error": f"{func_name}: There is no response text. This could be due to safety or copyright issues."}

    except Exception as e:
        func_name = inspect.currentframe().f_code.co_name
        logger.error(f"Error generating AI analysis report using Gemini '{func_name}': {e}")
        raise {f"{func_name}: Error": e.args[0]}
