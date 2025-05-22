from typing import List

from fastapi import HTTPException, status
from reportlab.pdfgen import canvas
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import logger
from com.curds.Metric import create_metric, create_metrics
from com.models.Tone import Tone as SQLTone
from com.models.Report import Report as SQLReport
from com.models.Result import Result as SQLResult
from com.models.Metric import Metric as SQLMetric
from com.schemas.report import Report
from com.schemas.result import ResultCreate, Result
from com.utils import Helper
from com.utils.Metrice import extract_min_max, matric_string_to_dict


def generate_pdf_report(analysis_dict: dict, output_path: str):
    """Generates a PDF report from the analysis results."""
    c = canvas.Canvas(output_path)
    c.drawString(100, 750, "Analysis Report")
    c.drawString(100, 700, f"Summary: {analysis_dict['summary']}")
    c.drawString(100, 650, "Lifestyle Changes:")
    y = 630
    for change in analysis_dict['lifestyle_changes']:
        c.drawString(120, y, f"- {change}")
        y -= 20

    c.drawString(100, y, "Diet Routine:")
    y -= 20
    for routine in analysis_dict['diet_routine']:
        c.drawString(120, y, f"- {routine}")
        y -= 20
    c.save()


def save_report(report_data: dict, db: Session):
    """
    Saves a new report to the database based on extracted text data.

    Args:
        report_data (dict): A dictionary containing the extracted report data.
                                  Expected keys: 'name', 'location' (optional), 'content' (optional).
        db (Session): The database session.

    Returns:
        Report: The created report object.

    Raises:
        HTTPException (status_code=400): If the report name is missing.
        HTTPException (status_code=500): If there's a database error.
    """
    name = report_data.get("name")
    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report name is required."
        )

    db_report = SQLReport(
        id=report_data.get("id"),
        name=report_data.get("name"),
        location=report_data.get("location"),
        user_id=report_data.get("user_id"),
        content=report_data.get("content"),
        report_type=report_data.get("report_type")
    )

    try:
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        return Report.from_orm(report_data)
    except IntegrityError as e:
        logger.info(f"DB IntegrityError {e.args[0]}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while saving report: {e}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while saving report: {e}"
        )


def save_analysis_result(result_data: dict, db: Session):
    """
    Saves the analysis result to the database.

    Args:
        result_data (ResultCreate): Pydantic schema containing the result data.
        db (Session): The database session.

    Returns:
        Result: The created result object.
    """

    result_id = Helper.generate_id()
    db_result = SQLResult(
        id=result_id,
        result=result_data.get("result"),
        report_id=result_data.get("report_id"),
        tone_id=result_data.get("tone_id"),
        language=result_data.get("language")
    )
    try:
        db.add(db_result)
        db.commit()
        db.refresh(db_result)

        # Save metrics
        detailed_results = find_detailed_results(result_data)
        if detailed_results is not None:
            metrics_to_create: List[SQLMetric] = []
            detailed_results_metrics = matric_string_to_dict(detailed_results)
            report_id = result_data.get("report_id")  # Assuming report_id is the same for all detailed results
            for metric_item in detailed_results_metrics:
                metric_id = Helper.generate_id()
                min_max_range = extract_min_max(str(metric_item))
                db_metric = SQLMetric(
                    id=metric_id,
                    name=metric_item.get("name"),
                    value=metric_item.get("value") if isinstance(metric_item.get("value"), str) else str(
                        metric_item.get("value")),
                    unit=metric_item.get("unit"),
                    reference_range_min=min_max_range.get("min"),
                    reference_range_max=min_max_range.get("max"),
                    status=metric_item.get("status"),
                    report_id=report_id,
                    result_id=result_id
                )
                metrics_to_create.append(db_metric)
            saved_metrics = create_metrics(db=db, metrics=metrics_to_create)

        return Result.from_orm(db_result)
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Database integrity error while saving analysis result: {e.args[0]}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database integrity error while saving analysis result: {e}"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Exception error while saving analysis result: {e.args[0]}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while saving analysis result: {e}"
        )


def detect_report_type(extracted_text: str):
    """
    Rudimentary function to detect report type from text.
    This is a placeholder and needs a more robust implementation.
    """
    text_lower = extracted_text.lower()
    if "complete blood count" in text_lower or "cbc" in text_lower:
        return "cbc"
    elif "compare" in text_lower and "blood test" in text_lower:
        return "compare"
    elif "blood glucose" in text_lower or "sugar level" in text_lower:
        return "glucose"
    elif "liver function test" in text_lower or "lfts" in text_lower:
        return "liver"
    elif "kidney function test" in text_lower or "creatinine" in text_lower or "bun" in text_lower:
        return "kidney"
    elif "lipid profile" in text_lower or "cholesterol" in text_lower or "ldl" in text_lower or "hdl" in text_lower or "triglycerides" in text_lower:
        return "lipid"
    elif "hemoglobin a1c" in text_lower or "hba1c" in text_lower:
        return "hba1c"
    elif "vitamin d" in text_lower or "25-hydroxy vitamin d" in text_lower:
        return "vitamin_d"
    elif "thyroid function test" in text_lower or "tsh" in text_lower or "t3" in text_lower or "t4" in text_lower:
        return "thyroid"
    elif "iron" in text_lower and "ferritin" in text_lower:
        return "iron"
    elif "c-reactive protein" in text_lower or "crp" in text_lower or "erythrocyte sedimentation rate" in text_lower or "esr" in text_lower:
        return "inflammation"

    return text_lower


import json

def find_detailed_results(data):
    """
    Checks if a dictionary or a JSON string contains the key "detailed_results"
    at any level and returns its value as a JSON string.

    Args:
        data: A dictionary or a JSON formatted string.

    Returns:
        A JSON string representing the value of "detailed_results" if found,
        otherwise None.
    """
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return None  # Invalid JSON string

    if isinstance(data, dict):
        if "detailed_results" in data:
            return json.dumps(data["detailed_results"])
        for value in data.values():
            result = find_detailed_results(value)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_detailed_results(item)
            if result:
                return result
    return None

# # Your dictionary object as a string
# data_string = '{"result": "{\\"summary\\": \\"The patient\'s erythrocyte sedimentation rate (ESR) is significantly elevated, indicating potential inflammation.\\u00a0 The provided CRP value is missing.\\", \\"detailed_results\\": {\\"ESR\\": {\\"value\\": {\\"first_hour\\": 38, \\"second_hour\\": 75}, \\"unit\\": \\"mms\\", \\"normal_range\\": \\"Up to 10 mms (first hour), Up to 20 mms (second hour)\\", \\"status\\": \\"high\\"}}, \\"interpretation\\": \\"The ESR results are markedly elevated, strongly suggesting the presence of inflammation in the body.\\u00a0 The absence of a CRP value prevents a complete assessment of the inflammatory process.\\u00a0 The high ESR could indicate various conditions.\\", \\"potential causes\\": [\\"Infection (bacterial, viral, or fungal)\\", \\"Autoimmune diseases (rheumatoid arthritis, lupus)\\", \\"Inflammation of tissues (e.g., vasculitis)\\", \\"Malignancy\\", \\"Tissue damage or necrosis\\", \\"Anemia\\", \\"Certain medications\\"], \\"next steps\\": [\\"A complete blood count (CBC) should be ordered to further investigate potential causes of the elevated ESR.\\", \\"CRP testing is crucial to obtain a more comprehensive picture of the inflammatory process.\\u00a0 A high CRP would strengthen the indication of inflammation.\\", \\"The patient should consult a physician to discuss the elevated ESR and potential underlying causes. Further investigations, such as imaging studies or specialized blood tests, might be necessary to identify the specific condition.\\" ]}, \\"report_id\\": \\"1xKCKezE70g5uI\\", \\"tone_id\\": \\"general\\", \\"language\\": \\"en\\"}"}'
#
# # Parse the main JSON string
# try:
#     main_data = json.loads(data_string)
# except json.JSONDecodeError:
#     print("Error: Invalid main JSON string")
#     main_data = None

# if main_data:
#     detailed_results_json = find_detailed_results(main_data)
#
#     if detailed_results_json:
#         print(detailed_results_json)
#     else:
#         print("Key 'detailed_results' not found at any level.")
