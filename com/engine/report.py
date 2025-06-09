import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from com.models.Report import Report as SQLReport
from com.models.Result import Result as SQLResult
from com.models.Metric import Metric as SQLMetric
from com.schemas.analysisResult import AnalysisResult, AnalysisDetailedResultItem
from com.schemas.report import ReportCard as ReportCard


def get_report_cards(db, user_id: str, tone: str = "general") -> list[dict]:
    report_cards = []
    db_report = db.query(SQLReport).filter(SQLReport.user_id == user_id).all()

    for report in db_report:
        db_result = db.query(SQLResult).filter(
            SQLResult.report_id == report.id,
            SQLResult.tone_id == tone
        ).first()

        if db_result:
            db_metrics = db.query(SQLMetric).filter(
                SQLMetric.result_id == db_result.id
            ).all()

            metrics = [
                {
                    "name": str(m.name),
                    "value": str(m.value),
                    "unit": str(m.unit) if m.unit is not None else "None",
                    "reference_range_min": str(m.reference_range_min),
                    "reference_range_max": str(m.reference_range_max),
                    "status": str(m.status),
                    "result_id": str(m.result_id),
                }
                for m in db_metrics
            ]
        else:
            metrics = []

        card = {
            "id": str(report.id),
            "report_name": str(report.name),
            "report_date": report.added_datetime.isoformat() if hasattr(report.added_datetime, 'isoformat') else str(
                report.added_datetime),
            "status": report.status,
            "metrics": metrics
        }
        report_cards.append(card)

    return report_cards


def get_parsed_report_analysis_for_user(
    db,
    user_id: str,
    report_id: str
) -> Optional[AnalysisResult]:
    """
    Retrieves and processes the overall report analysis (summary, detailed results, etc.)
    for a given report ID and user ID, including the report name.
    """
    # Fetch the specific SQLResult object, and the associated SQLReport object.
    # We explicitly select SQLReport here to get its name.
    main_result_data = db.query(
        SQLResult,
        SQLReport.name # --- NEW: Select report_name ---
    ).join(
        SQLReport, SQLResult.report_id == SQLReport.id
    ).filter(
        SQLReport.user_id == user_id,
        SQLResult.report_id == report_id
    ).first() # Use .first() as we expect one primary result for the analysis

    if not main_result_data:
        return None # No data found for this user/report combination

    main_result_obj = main_result_data[0] # The SQLResult object
    report_name = main_result_data[1] # --- NEW: Get the report name ---

    if not main_result_obj.result:
        return None # No analysis content found

    try:
        parsed_analysis_dict = json.loads(main_result_obj.result)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error parsing nested JSON from result.result: {e}")
        return None

    ai_detailed_results: Dict[str, AnalysisDetailedResultItem] = {}
    if 'detailed_results' in parsed_analysis_dict and isinstance(parsed_analysis_dict['detailed_results'], dict):
        for metric_name, metric_data in parsed_analysis_dict['detailed_results'].items():
            ai_detailed_results[metric_name] = AnalysisDetailedResultItem(**metric_data)

    # Construct the AnalysisResult instance, including the report_name
    overall_analysis = AnalysisResult(
        report_name=report_name, # --- NEW: Pass report_name here ---
        summary=parsed_analysis_dict.get('summary'),
        detailed_results=ai_detailed_results,
        recommendations=parsed_analysis_dict.get('recommendations'),
        potential_implications=parsed_analysis_dict.get('interpretation'),
        lifestyle_changes=parsed_analysis_dict.get('lifestyle_changes'),
        diet_routine=parsed_analysis_dict.get('diet_routine'),
        key_findings=parsed_analysis_dict.get('key_findings'),
        potential_impact=parsed_analysis_dict.get('potential_impact'),
        detailed_analysis=parsed_analysis_dict.get('detailed_analysis'), # Ensure all fields are mapped
        potential_causes=parsed_analysis_dict.get('potential_causes'),
        next_steps=parsed_analysis_dict.get('next_steps'),
        disclaimer=parsed_analysis_dict.get('disclaimer'),
        result_explanations=parsed_analysis_dict.get('result_explanations'),
        reference_ranges=parsed_analysis_dict.get('reference_ranges'),
        wellness_assessment=parsed_analysis_dict.get('wellness_assessment'),
        preventative_recommendations=parsed_analysis_dict.get('preventative_recommendations'),
        long_term_outlook=parsed_analysis_dict.get('long_term_outlook'),
        detailed_lab_values=parsed_analysis_dict.get('detailed_lab_values'),
        scientific_references=parsed_analysis_dict.get('scientific_references'),
        pathophysiological_explanations=parsed_analysis_dict.get('pathophysiological_explanations'),
        personal_summary=parsed_analysis_dict.get('personal_summary'),
        emotional_support=parsed_analysis_dict.get('emotional_support'),
        individualized_recommendations=parsed_analysis_dict.get('individualized_recommendations'),
        doctor_questions=parsed_analysis_dict.get('doctor_questions'),
        date=main_result_obj.added_datetime or datetime.now()
    )

    return overall_analysis
