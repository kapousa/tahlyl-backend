from fastapi import FastAPI, HTTPException, Body, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import datetime

from sqlalchemy.orm import Session

from com.curds.Metric import get_unique_metric_names_from_list
from config import get_sqlite_db_sync

# --- Common Helper for Disclaimers ---
MEDICAL_DISCLAIMER = (
    "Disclaimer: This information is for educational and informational purposes only, "
    "and does not constitute medical advice, diagnosis, or treatment. "
    "Always consult with a qualified healthcare professional for any health concerns or before making any decisions related to your health or treatment."
)

def analyze_health_trends(historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Placeholder for AI logic to analyze health trends."""
    # This would involve time-series analysis, anomaly detection, etc.
    # Example: looking at 'glucose' levels over time
    trends = {}
    metrics_list = get_unique_metric_names_from_list(historical_data)
    for metric in metrics_list: #["glucose", "cholesterol_ldl", "blood_pressure_systolic"]:
        values = [d.get(metric) for d in historical_data if d.get(metric) is not None]
        if len(values) > 1:
            if values[-1] > values[0]:
                trends[metric] = f"Your {metric.replace('_', ' ')} shows an increasing trend."
            elif values[-1] < values[0]:
                trends[metric] = f"Your {metric.replace('_', ' ')} shows a decreasing trend."
            else:
                trends[metric] = f"Your {metric.replace('_', ' ')} has remained stable."
        else:
            trends[metric] = f"Not enough data to determine a trend for {metric.replace('_', ' ')}."

    return {"trends": trends, "summary": "Identified some trends in your historical data.",
            "disclaimer": MEDICAL_DISCLAIMER}

def assess_risk(patient_data: Dict[str, Any]) -> Dict[str, Any]:
    """Placeholder for AI logic to assess health risks."""
    # This would use statistical models or ML classifiers
    # based on demographics, test results, etc.
    risk_factors = []
    if patient_data.get("age", 0) > 50 and patient_data.get("cholesterol_ldl", 0) > 130:
        risk_factors.append("Elevated LDL cholesterol is a risk factor for cardiovascular disease.")
    if patient_data.get("gender") == "female" and patient_data.get("iron_levels", 0) < 60:
        risk_factors.append("Low iron levels might indicate anemia, common in females.")

    # This is a highly simplified example. Real risk assessment is complex.
    return {"risk_assessment": risk_factors if risk_factors else [
        "No specific high risks identified based on provided data."], "disclaimer": MEDICAL_DISCLAIMER}

def recommend_lifestyle(health_data: Dict[str, Any]) -> Dict[str, Any]:
    """Placeholder for AI logic to generate personalized lifestyle recommendations."""
    recommendations = []
    if health_data.get("glucose") and health_data["glucose"] > 100:
        recommendations.append(
            "Consider reducing intake of sugary foods and drinks. Increase fiber-rich vegetables.")
    if health_data.get("cholesterol_ldl") and health_data["cholesterol_ldl"] > 130:
        recommendations.append(
            "Focus on a diet rich in fruits, vegetables, and whole grains. Incorporate healthy fats like avocado and nuts.")
    if health_data.get("blood_pressure_systolic") and health_data["blood_pressure_systolic"] > 120:
        recommendations.append(
            "Regular physical activity (e.g., brisk walking 30 mins/day) and stress management techniques can be beneficial.")

    return {"recommendations": recommendations if recommendations else [
        "Based on the data, general healthy lifestyle practices are recommended."],
            "disclaimer": MEDICAL_DISCLAIMER}

def generate_doctor_questions(analysis_summary: str, key_findings: List[str]) -> Dict[str, Any]:
    """Placeholder for AI logic to generate questions for doctors."""
    questions = [
        f"Can you explain '{key_findings[0]}' in more detail?",
        "Are there any specific lifestyle changes I should make based on these results?",
        "Do I need any follow-up tests or appointments?",
        "What do these results mean for my long-term health?"
    ]
    if "elevated glucose" in analysis_summary.lower() or "high glucose" in key_findings:
        questions.append("What are the next steps if my glucose levels remain elevated?")

    return {"suggested_questions": questions, "disclaimer": MEDICAL_DISCLAIMER}

def get_marker_deep_dive(marker_name: str) -> Dict[str, Any]:
    """Placeholder for AI logic to provide deep dive on a specific marker."""
    # This would pull from a comprehensive medical knowledge base
    marker_info = {
        "glucose": {
            "what_it_measures": "Glucose is a type of sugar and your body's main source of energy. It comes from the food you eat.",
            "why_important": "Maintaining healthy glucose levels is crucial for energy production and preventing conditions like diabetes.",
            "high_levels_indicate": "High glucose can indicate prediabetes, diabetes, or insulin resistance. It can also be temporarily elevated after meals or due to stress.",
            "low_levels_indicate": "Low glucose (hypoglycemia) can be caused by certain medications, excessive alcohol, or specific medical conditions."
        },
        "cholesterol_ldl": {
            "what_it_measures": "LDL (Low-Density Lipoprotein) cholesterol is often called 'bad' cholesterol because high levels can lead to plaque buildup in arteries.",
            "why_important": "High LDL cholesterol increases your risk for heart disease and stroke.",
            "high_levels_indicate": "High LDL levels are often linked to diet, genetics, and lack of physical activity.",
            "low_levels_indicate": "Extremely low LDL levels are rare but can be associated with certain genetic disorders or medical conditions."
        }
        # ... add more markers
    }
    info = marker_info.get(marker_name.lower().replace(" ", "_"),
                           {"error": "Marker not found or detailed info not available."})
    info["disclaimer"] = MEDICAL_DISCLAIMER
    return info

def get_comparison_with_ranges(marker_name: str, value: Any, age: int, gender: str) -> Dict[str, Any]:
    """Placeholder for AI logic to compare marker with contextual ranges."""
    # In a real system, these ranges would come from a database or a more complex model
    ranges = {
        "glucose": {"normal": (70, 100), "prediabetes": (101, 125), "diabetes": (126, 999)},
        "cholesterol_ldl": {"optimal": (0, 100), "near_optimal": (101, 129), "borderline_high": (130, 159),
                            "high": (160, 189), "very_high": (190, 999)}
    }

    result = {"marker": marker_name, "value": value}
    if marker_name.lower().replace(" ", "_") in ranges:
        marker_ranges = ranges[marker_name.lower().replace(" ", "_")]

        status = "Unknown"
        explanation = "No specific explanation available for this marker's range."

        for key, (lower, upper) in marker_ranges.items():
            if lower <= value <= upper:
                status = key.replace("_", " ").title()
                break

        if marker_name.lower() == "glucose":
            if status == "Normal":
                explanation = "Your glucose level is within the healthy fasting range."
            elif status == "Prediabetes":
                explanation = "Your glucose level indicates prediabetes, which means your blood sugar is higher than normal but not yet high enough for a diagnosis of type 2 diabetes. Lifestyle changes are often recommended."
            elif status == "Diabetes":
                explanation = "Your glucose level indicates diabetes. Please consult your doctor for diagnosis and management."
        elif marker_name.lower() == "cholesterol_ldl":
            if status == "Optimal":
                explanation = "Your LDL cholesterol level is considered optimal for heart health."
            elif status == "Borderline High" or status == "High" or status == "Very High":
                explanation = "Your LDL cholesterol level is elevated, which can increase the risk of cardiovascular disease. Lifestyle changes and medical consultation may be advised."

        result["status"] = status
        result["explanation"] = explanation
    else:
        result["status"] = "N/A"
        result["explanation"] = "Ranges for this marker are not available or not applicable for context."

    result["disclaimer"] = MEDICAL_DISCLAIMER
    return result



