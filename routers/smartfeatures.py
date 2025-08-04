from http.client import HTTPException
from fastapi import APIRouter, Body
from com.services.smartFeatures import assess_risk, get_comparison_with_ranges
from com.schemas.smartFeatures import FriendlyAnalysisOutput, ToneAnalysisInput, TrendAnalysisOutput, HealthTrendInput, \
    RiskAssessmentOutput, RiskAssessmentInput, LifestyleRecommendationOutput, LifestyleRecommendationInput, \
    DoctorQuestionsOutput, DoctorQuestionsInput, MarkerDeepDiveOutput, MarkerDeepDiveInput, MarkerComparisonOutput, \
    MarkerComparisonInput
from config import logger

router = APIRouter(prefix="/smartfeatures", tags=["smartfeatures"])


@router.get("/")
async def base_smart_features():
    logger.info("Base smart features endpoint hit.")
    return {"Hello": "Smart Features"}


@router.post("/analyze-health-trends/", response_model=TrendAnalysisOutput)
async def analyze_health_trends(
        input_data: HealthTrendInput = Body(
            ...,
            examples={
                "example": {
                    "summary": "Example for health trends",
                    "value": {
                        "historical_data": [
                            {"date": "2023-01-15", "test_name": "Blood Panel",
                             "metrics": {"glucose": 90, "cholesterol_ldl": 110}},
                            {"date": "2023-07-20", "test_name": "Blood Panel",
                             "metrics": {"glucose": 95, "cholesterol_ldl": 125}},
                            {"date": "2024-01-25", "test_name": "Blood Panel",
                             "metrics": {"glucose": 105, "cholesterol_ldl": 140}}
                        ]
                    }
                }
            }
        )
):
    """
    Analyzes historical medical test data to identify trends over time.
    """
    try:
        trend_analysis = analyze_health_trends([item.model_dump() for item in input_data.historical_data])
        return trend_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing trends: {e}")


@router.post("/assess-health-risk/", response_model=RiskAssessmentOutput)
async def assess_health_risk(
        input_data: RiskAssessmentInput = Body(
            ...,
            examples={
                "example": {
                    "summary": "Example for risk assessment",
                    "value": {
                        "patient_data": {
                            "age": 55,
                            "gender": "male",
                            "cholesterol_ldl": 185,
                            "blood_pressure_systolic": 150,
                            "family_history_diabetes": True
                        }
                    }
                }
            }
        )
):
    """
    Provides a personalized health risk assessment based on patient data.
    (Highly simplified example - real risk assessment is complex and requires specialized models).
    """
    try:
        risk_assessment = assess_risk(input_data.patient_data)
        return risk_assessment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assessing risk: {e}")


@router.post("/recommend-lifestyle/", response_model=LifestyleRecommendationOutput)
async def recommend_lifestyle(
        input_data: LifestyleRecommendationInput = Body(
            ...,
            examples={
                "example": {
                    "summary": "Example for lifestyle recommendations",
                    "value": {
                        "health_data": {
                            "glucose": 115,
                            "cholesterol_ldl": 145,
                            "blood_pressure_systolic": 135
                        }
                    }
                }
            }
        )
):
    """
    Generates personalized nutrition and lifestyle recommendations based on health metrics.
    """
    try:
        recommendations = recommend_lifestyle(input_data.health_data)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {e}")


@router.post("/generate-doctor-questions/", response_model=DoctorQuestionsOutput)
async def generate_doctor_questions(
        input_data: DoctorQuestionsInput = Body(
            ...,
            examples={
                "example": {
                    "summary": "Example for doctor questions",
                    "value": {
                        "analysis_summary": "Your recent blood test shows elevated glucose and LDL cholesterol levels.",
                        "key_findings": ["Elevated Glucose", "High LDL Cholesterol"]
                    }
                }
            }
        )
):
    """
    Generates a list of relevant questions a user might ask their doctor.
    """
    try:
        questions = generate_doctor_questions(input_data.analysis_summary, input_data.key_findings)
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {e}")


@router.post("/get-marker-deep-dive/", response_model=MarkerDeepDiveOutput)
async def get_marker_deep_dive(
        input_data: MarkerDeepDiveInput = Body(
            ...,
            examples={
                "glucose": {
                    "summary": "Example for Glucose deep dive",
                    "value": {"marker_name": "Glucose"}
                },
                "ldl_cholesterol": {
                    "summary": "Example for LDL Cholesterol deep dive",
                    "value": {"marker_name": "LDL Cholesterol"}
                }
            }
        )
):
    """
    Provides an in-depth explanation of a specific medical marker.
    """
    try:
        deep_dive = get_marker_deep_dive(input_data.marker_name)
        return deep_dive
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving marker info: {e}")


@router.post("/compare-marker-with-ranges/", response_model=MarkerComparisonOutput)
async def compare_marker_with_ranges(
        input_data: MarkerComparisonInput = Body(
            ...,
            examples={
                "high_glucose": {
                    "summary": "Example for high Glucose",
                    "value": {
                        "marker_name": "Glucose",
                        "value": 110,
                        "age": 40,
                        "gender": "female"
                    }
                },
                "normal_ldl": {
                    "summary": "Example for normal LDL",
                    "value": {
                        "marker_name": "Cholesterol LDL",
                        "value": 90,
                        "age": 35,
                        "gender": "male"
                    }
                }
            }
        )
):
    """
    Compares a specific marker's value against contextual healthy ranges (e.g., by age/gender).
    """
    try:
        comparison_result = get_comparison_with_ranges(
            input_data.marker_name,
            input_data.value,
            input_data.age,
            input_data.gender
        )
        return comparison_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing marker with ranges: {e}")
