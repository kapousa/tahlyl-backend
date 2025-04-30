from typing import Optional

from fastapi import HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from config import get_db
from lib.models import Report as SQLReport
from lib.models import Result as SQLResult
from lib.schemas.report import Report
from lib.schemas.result import ResultCreate, Result


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

def save_report(report_data: dict, user_id: str, db):
    """
    Saves a new report to the database based on extracted text data.

    Args:
        report_data (dict): A dictionary containing the extracted report data.
                                  Expected keys: 'name', 'location' (optional), 'content' (optional).
        user_id (str): The ID of the user who owns the report.
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
        id=str(uuid4()),
        name=report_data.name,
        location=report_data.location,
        user_id=report_data.user_id,
        content=report_data.content
    )

    try:
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        return Report.from_orm(db_report)
    except IntegrityError as e:
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

def save_analysis_result(result_data: ResultCreate, db: Session):
    """
    Saves the analysis result to the database.

    Args:
        result_data (ResultCreate): Pydantic schema containing the result data.
        db (Session): The database session.

    Returns:
        Result: The created result object.
    """
    db_result = SQLResult(
        id=str(uuid4()),
        result=result_data.result,
        report_id=result_data.report_id,
        tone_id=result_data.tone_id,
    )
    try:
        db.add(db_result)
        db.commit()
        db.refresh(db_result)
        return Result.from_orm(db_result)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database integrity error while saving analysis result: {e}"
        )
    except Exception as e:
        db.rollback()
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
