# --- Pydantic Models for Request/Response Bodies ---
from datetime import datetime
from typing import Any, List, Optional, Dict

from pydantic import BaseModel, Field, ConfigDict


class MedicalReportInput(BaseModel):
    report_text: str = Field(..., description="The raw text content of the medical test report.")


class FriendlyAnalysisOutput(BaseModel):
    analysis: str
    disclaimer: str


class ToneAnalysisInput(MedicalReportInput):
    tone: str = Field(..., description="Desired tone for the analysis (general, doctor, educational).")


class HistoricalDataItem(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    date: datetime.date = Field(..., description="Date of the medical test.")
    test_name: str = Field(..., description="Name of the test (e.g., 'Blood Panel').")
    # Using Any for value as it can be numeric or a string (e.g., 'Positive', 'Negative')
    # For numerical analysis, you'd extract specific metrics.
    metrics: Dict[str, Any] = Field(...,
                                    description="Dictionary of specific metrics and their values (e.g., {'glucose': 95, 'cholesterol_ldl': 120}).")


class HealthTrendInput(BaseModel):
    historical_data: List[HistoricalDataItem] = Field(..., description="A list of historical medical test results.")


class TrendAnalysisOutput(BaseModel):
    trends: Dict[str, Any]
    summary: str
    disclaimer: str


class PatientDemographics(BaseModel):
    age: int
    gender: str  # e.g., "male", "female", "other"
    # Add other relevant demographics like pre-existing conditions, family history etc. if available
    # For this example, we'll keep it simple


class RiskAssessmentInput(BaseModel):
    patient_data: Dict[str, Any] = Field(...,
                                         description="Combined data for risk assessment (e.g., {'age': 45, 'gender': 'female', 'cholesterol_ldl': 180, 'blood_pressure_systolic': 145}).")


class RiskAssessmentOutput(BaseModel):
    risk_assessment: List[str]
    disclaimer: str


class LifestyleRecommendationInput(BaseModel):
    health_data: Dict[str, Any] = Field(...,
                                        description="Key health metrics for recommendations (e.g., {'glucose': 110, 'cholesterol_ldl': 140}).")


class LifestyleRecommendationOutput(BaseModel):
    recommendations: List[str]
    disclaimer: str


class DoctorQuestionsInput(BaseModel):
    analysis_summary: str = Field(..., description="A summary of the medical report analysis.")
    key_findings: List[str] = Field(..., description="List of important findings from the report.")


class DoctorQuestionsOutput(BaseModel):
    suggested_questions: List[str]
    disclaimer: str


class MarkerDeepDiveInput(BaseModel):
    marker_name: str = Field(...,
                             description="The name of the medical marker to get detailed information about (e.g., 'Glucose', 'LDL Cholesterol').")


class MarkerDeepDiveOutput(BaseModel):
    what_it_measures: Optional[str]
    why_important: Optional[str]
    high_levels_indicate: Optional[str]
    low_levels_indicate: Optional[str]
    error: Optional[str]
    disclaimer: str


class MarkerComparisonInput(BaseModel):
    marker_name: str = Field(..., description="The name of the medical marker (e.g., 'Glucose').")
    value: Any = Field(..., description="The value of the marker.")
    age: int = Field(..., description="Patient's age.")
    gender: str = Field(..., description="Patient's gender (e.g., 'male', 'female').")


class MarkerComparisonOutput(BaseModel):
    marker: str
    value: Any
    status: str
    explanation: str
    disclaimer: str