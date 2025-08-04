from typing import List
from fastapi import HTTPException, status
from reportlab.pdfgen import canvas
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from config import logger
from com.services.metric import create_metrics
from com.models.Report import Report as SQLReport
from com.models.Result import Result as SQLResult
from com.models.Metric import Metric as SQLMetric
from com.schemas.report import Report
from com.schemas.result import ResultCreate, Result
from com.utils import Helper
from com.utils.Metrice import extract_min_max, matric_string_to_dict
import json


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


def detect_report_type_limitied(extracted_text: str):
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

def detect_report_type(extracted_text: str):
    """
    Detects the type of health report from the extracted text.

    This function uses a rule-based approach with an expanded set of keywords
    and prioritizes more specific matches.

    Args:
        extracted_text (str): The full text extracted from the health report.

    Returns:
        str: A standardized string representing the detected report type
             (e.g., "cbc", "liver", "glucose", "unknown"), or "other_blood_test"
             for general blood tests not specifically matched.
    """
    text_lower = extracted_text.lower()

    # --- Highly Specific Tests (Prioritize these) ---

    # Glucose-related tests
    if "hemoglobin a1c" in text_lower or "hba1c" in text_lower:
        return "hba1c"
    elif "oral glucose tolerance test" in text_lower or "ogtt" in text_lower:
        return "ogtt" # New specific type
    elif "blood glucose" in text_lower or "sugar level" in text_lower or "fasting glucose" in text_lower or "random glucose" in text_lower:
        return "glucose"

    # Liver Function Tests
    elif "liver function test" in text_lower or "lfts" in text_lower or "hepatic panel" in text_lower or "alt" in text_lower or "ast" in text_lower or "alkaline phosphatase" in text_lower or "bilirubin" in text_lower:
        return "liver"

    # Kidney Function Tests
    elif "kidney function test" in text_lower or "renal function test" in text_lower or "kfts" in text_lower or "rfts" in text_lower or "creatinine" in text_lower or "bun" in text_lower or "egfr" in text_lower or "glomerular filtration" in text_lower:
        return "kidney"

    # Lipid Profile / Cholesterol
    elif "lipid profile" in text_lower or "cholesterol" in text_lower or "ldl" in text_lower or "hdl" in text_lower or "triglycerides" in text_lower or "atherogenic index" in text_lower:
        return "lipid"

    # Thyroid Function Tests
    elif "thyroid function test" in text_lower or "tsh" in text_lower or "t3" in text_lower or "t4" in text_lower or "free t3" in text_lower or "free t4" in text_lower:
        return "thyroid"

    # Complete Blood Count / Hemogram
    elif "complete blood count" in text_lower or "cbc" in text_lower or "full blood count" in text_lower or "fbc" in text_lower or "hemogram" in text_lower or "white blood cell" in text_lower or "red blood cell" in text_lower or "platelet count" in text_lower or "hemoglobin" in text_lower:
        return "cbc"

    # Inflammation Markers
    elif "c-reactive protein" in text_lower or "crp" in text_lower or "erythrocyte sedimentation rate" in text_lower or "esr" in text_lower or "inflammation marker" in text_lower:
        return "inflammation"

    # Vitamin & Mineral Tests
    elif "vitamin d" in text_lower or "25-hydroxy vitamin d" in text_lower or "cholecalciferol" in text_lower:
        return "vitamin_d"
    elif "iron panel" in text_lower or "iron studies" in text_lower or "ferritin" in text_lower or "transferrin" in text_lower or "iron binding capacity" in text_lower:
        return "iron"
    elif "vitamin b12" in text_lower or "cobalamin" in text_lower: # New specific type
        return "vitamin_b12"
    elif "folate" in text_lower or "folic acid" in text_lower: # New specific type
        return "folate"

    # Electrolytes & Basic Metabolic Panel
    elif "electrolyte" in text_lower or "sodium" in text_lower or "potassium" in text_lower or "chloride" in text_lower or "bicarbonate" in text_lower or "co2 content" in text_lower:
        return "electrolytes" # New specific type
    elif "basic metabolic panel" in text_lower or "bmp" in text_lower:
        return "bmp" # New specific type (often includes glucose, kidney, electrolytes)
    elif "comprehensive metabolic panel" in text_lower or "cmp" in text_lower:
        return "cmp" # New specific type (more comprehensive than BMP)

    # Coagulation / Blood Clotting Tests
    elif "prothrombin time" in text_lower or "pt/inr" in text_lower or "inr" in text_lower or "partial thromboplastin time" in text_lower or "aptt" in text_lower or "coagulation panel" in text_lower:
        return "coagulation" # New specific type

    # Hormone Tests (general or specific examples)
    elif "testosterone" in text_lower or "estrogen" in text_lower or "hormone panel" in text_lower:
        return "hormone" # New broader hormone category

    # Urine Tests
    elif "urinalysis" in text_lower or "urine test" in text_lower or "urine culture" in text_lower:
        return "urinalysis" # New broader urine category

    # Imaging Reports (common types)
    elif "x-ray" in text_lower or "radiograph" in text_lower:
        return "xray" # New type
    elif "mri" in text_lower or "magnetic resonance imaging" in text_lower:
        return "mri" # New type
    elif "ct scan" in text_lower or "computed tomography" in text_lower:
        return "ct_scan" # New type
    elif "ultrasound" in text_lower or "sonography" in text_lower:
        return "ultrasound" # New type
    elif "ecg" in text_lower or "ekg" in text_lower or "electrocardiogram" in text_lower:
        return "ecg" # New type (often considered imaging/diagnostic)

    # General Reports (less specific, put lower in hierarchy)
    elif "compare" in text_lower and "blood test" in text_lower:
        return "compare_blood_test" # Renamed for clarity
    elif "blood test result" in text_lower or "lab result" in text_lower or "laboratory report" in text_lower:
        return "other_blood_test" # More generic blood test if nothing specific found
    elif "medical report" in text_lower or "patient record" in text_lower or "consultation notes" in text_lower:
        return "general_medical_report" # New generic medical report type

    # Default if no specific type is detected
    return "unknown" # Changed default to 'unknown' for clarity

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
