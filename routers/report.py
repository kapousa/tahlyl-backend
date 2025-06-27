from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, APIRouter, Depends
import datetime

from sqlalchemy.orm import Session
from starlette import status

from com.engine.report import get_report_cards, get_parsed_report_analysis_for_user
from com.engine.auth.jwt_security import get_current_user
from com.schemas.user import User
from config import get_db

router = APIRouter(prefix="/report", tags=["report"])

# Data Models using Pydantic
class ReferenceRange(BaseModel):
    min: float
    max: float

class Metric(BaseModel):
    name: str
    value: float
    unit: str
    referenceRange: ReferenceRange
    status: str  # e.g., "normal", "high", "low", "critical"

class BloodTest(BaseModel):
    id: int  # Add an ID for database retrieval
    name: str
    date: datetime.date
    status: str  # Overall test status
    metrics: List[Metric]

# Sample Data (In-memory storage for this example)
sample_blood_tests = [
    BloodTest(
        id=1,
        name="Complete Blood Count (CBC)",
        date=datetime.date(2024, 1, 15),
        status="normal",
        metrics=[
            Metric(name="White Blood Cells", value=7.5, unit="x10^9/L", referenceRange=ReferenceRange(min=4.0, max=11.0), status="normal"),
            Metric(name="Red Blood Cells", value=4.8, unit="x10^12/L", referenceRange=ReferenceRange(min=4.5, max=5.5), status="normal"),
            Metric(name="Hemoglobin", value=14.0, unit="g/dL", referenceRange=ReferenceRange(min=13.0, max=17.0), status="normal"),
            Metric(name="Platelets", value=250, unit="x10^9/L", referenceRange=ReferenceRange(min=150, max=400), status="normal"),
        ],
    ),
    BloodTest(
        id=2,
        name="Basic Metabolic Panel (BMP)",
        date=datetime.date(2024, 1, 20),
        status="abnormal",
        metrics=[
            Metric(name="Glucose", value=110, unit="mg/dL", referenceRange=ReferenceRange(min=70, max=100), status="high"),
            Metric(name="Sodium", value=140, unit="mEq/L", referenceRange=ReferenceRange(min=135, max=145), status="normal"),
            Metric(name="Potassium", value=5.2, unit="mEq/L", referenceRange=ReferenceRange(min=3.5, max=5.0), status="high"),
            Metric(name="Creatinine", value=1.5, unit="mg/dL", referenceRange=ReferenceRange(min=0.6, max=1.2), status="high"),
        ],
    ),
    BloodTest(
        id=3,
        name="Liver Function Test (LFT)",
        date=datetime.date(2024, 2, 10),
        status="normal",
        metrics=[
            Metric(name="ALT", value=25, unit="U/L", referenceRange=ReferenceRange(min=7, max=56), status="normal"),
            Metric(name="AST", value=30, unit="U/L", referenceRange=ReferenceRange(min=10, max=40), status="normal"),
            Metric(name="Bilirubin", value=0.8, unit="mg/dL", referenceRange=ReferenceRange(min=0.2, max=1.2), status="normal"),
            Metric(name="Albumin", value=4.5, unit="g/dL", referenceRange=ReferenceRange(min=3.4, max=5.4), status="normal"),
        ]
    ),
    BloodTest(
        id=4,
        name="Thyroid Function Test",
        date=datetime.date(2024, 2, 15),
        status="critical",
        metrics=[
            Metric(name="TSH", value=12.0, unit="µIU/mL", referenceRange=ReferenceRange(min=0.4, max=4.0), status="high"),
            Metric(name="T4", value=6.0, unit="µg/dL", referenceRange=ReferenceRange(min=4.5, max=12.0), status="normal"),
            Metric(name="T3", value=100, unit="ng/dL", referenceRange=ReferenceRange(min=80, max=200), status="normal"),
        ]
    ),
     BloodTest(
        id=5,
        name="Lipid Profile",
        date=datetime.date(2024, 3, 1),
        status="abnormal",
        metrics=[
            Metric(name="Total Cholesterol", value=240, unit="mg/dL", referenceRange=ReferenceRange(min=120, max=200), status="high"),
            Metric(name="HDL Cholesterol", value=40, unit="mg/dL", referenceRange=ReferenceRange(min=40, max=60), status="normal"),
            Metric(name="LDL Cholesterol", value=180, unit="mg/dL", referenceRange=ReferenceRange(min=0, max=100), status="high"),
            Metric(name="Triglycerides", value=200, unit="mg/dL", referenceRange=ReferenceRange(min=0, max=150), status="high"),
        ]
    )
]

# API Endpoints
@router.get("/blood_tests/", response_model=List[BloodTest])
async def get_blood_tests():
    """
    Retrieves a list of all blood tests.
    """
    return sample_blood_tests

@router.get("/blood_tests/{test_id}", response_model=BloodTest)
async def get_blood_test(test_id: int):
    """
    Retrieves a specific blood test by its ID.
    """
    for test in sample_blood_tests:
        if test.id == test_id:
            return test
    raise HTTPException(status_code=404, detail="Blood test not found")

#  Additional endpoints for download and share functionality can be added.  Since those actions
#  typically involve client-side (React) logic for file generation or sharing mechanisms,
#  the FastAPI backend might provide supporting data or URLs.  Here are example definitions:

@router.get("/blood_tests/{test_id}/download")
async def download_blood_test(test_id: int):
    """
    (Placeholder)  Simulates initiating a download of a blood test report.
    In a real application, this might generate a PDF or other file.  This simplified version returns the data.
    """
    for test in sample_blood_tests:
        if test.id == test_id:
            return test #  The actual implementation would generate a file and return it.
    raise HTTPException(status_code=404, detail="Blood test not found")
    #  In a full implementation, you'd use a library like reportlab or fpdf to generate a PDF.
    #  You'd then return the file using StreamingResponse.  This is beyond the scope of this basic example.

@router.get("/blood_tests/{test_id}/share")
async def share_blood_test(test_id: int):
    """
    (Placeholder) Simulates sharing a blood test (e.g., via email).
    In a real application, this might send an email with a link to the test result.
    """
    for test in sample_blood_tests:
        if test.id == test_id:
            #  Here, you might use an email sending library (e.g., sendgrid, email.mime) to send an email.
            #  For simplicity, we'll just return a message with the data.
            return {"message": f"Blood test data for test ID {test_id} would be shared (e.g., via email) in a real application.", "data": test}
    raise HTTPException(status_code=404, detail="Blood test not found")

@router.get("/cards")
async def fetch_report_cards_endpoint(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    report_cards = get_report_cards(db, user_id)
    return report_cards

    raise Exception(f"Cards Error ({e})")

@router.get("/{report_id}/analysis")
async def get_report_details(report_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Call the service function to get the parsed AnalysisResult object
    analysis_data = get_parsed_report_analysis_for_user(db, current_user.id, report_id)

    if not analysis_data:
        # If no data is returned, it means the report doesn't exist,
        # or doesn't belong to the user, or parsing failed.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report analysis not found or not accessible."
        )

    return analysis_data
