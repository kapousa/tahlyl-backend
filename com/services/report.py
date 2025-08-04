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
            "metrics": metrics,
            "report_type": report.report_type
        }
        report_cards.append(card)

    return report_cards

def get_general_report_analysis_for_user(
    db,
    user_id: str,
    report_id: str
) -> Optional[AnalysisResult]:
    """
    Retrieves and processes the overall report analysis (summary, detailed results, etc.)
    for a given report ID and user ID, specifically for the 'general' tone.
    """
    # Fetch the SQLResult object with tone_id = "general" and its associated SQLReport.
    main_result_data = db.query(
        SQLResult,
        SQLReport.name # Assuming SQLReport.name is the report_name field
    ).join(
        SQLReport, SQLResult.report_id == SQLReport.id
    ).filter(
        SQLReport.user_id == user_id,
        SQLResult.report_id == report_id,
        SQLResult.tone_id == "general" # Filter for 'general' tone_id
    ).first() # Use .first() as we expect only one 'general' tone result

    if not main_result_data:
        # No 'general' tone analysis found for this user/report.
        return None

    main_result_obj, report_name = main_result_data # Unpack the fetched data

    if not main_result_obj.result:
        # The 'result' field (AI analysis JSON) is empty.
        return None

    try:
        parsed_analysis_dict = json.loads(main_result_obj.result)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error parsing nested JSON from result.result: {e}")
        return None

    ai_detailed_results: Dict[str, AnalysisDetailedResultItem] = {}
    if 'detailed_results' in parsed_analysis_dict and isinstance(parsed_analysis_dict['detailed_results'], dict):
        for metric_name, metric_data in parsed_analysis_dict['detailed_results'].items():
            ai_detailed_results[metric_name] = AnalysisDetailedResultItem(**metric_data)

    # Construct the AnalysisResult instance
    overall_analysis = AnalysisResult(
        report_name=report_name,
        tone_id="general",
        summary=parsed_analysis_dict.get('summary'),
        detailed_results=ai_detailed_results,
        recommendations=parsed_analysis_dict.get('recommendations'),
        potential_implications=parsed_analysis_dict.get('interpretation'), # 'interpretation' from AI response
        lifestyle_changes=parsed_analysis_dict.get('lifestyle_changes'),
        diet_routine=parsed_analysis_dict.get('diet_routine'),
        key_findings=parsed_analysis_dict.get('key_findings'),
        potential_impact=parsed_analysis_dict.get('potential_impact'),
        detailed_analysis=parsed_analysis_dict.get('detailed_analysis'),
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

def get_all_report_analyses_for_user(
    db,
    user_id: str,
    report_id: str
) -> List[AnalysisResult]:
    """
    Retrieves and processes all report analysis records (summaries, detailed results, etc.)
    for a given report ID and user ID.
    """
    all_results_data = db.query(
        SQLResult,
        SQLReport.name # Assuming SQLReport.name is the report_name field
    ).join(
        SQLReport, SQLResult.report_id == SQLReport.id
    ).filter(
        SQLReport.user_id == user_id,
        SQLResult.report_id == report_id
    ).all()

    if not all_results_data:
        # No analysis records found for this user/report.
        return [] # Return an empty list

    parsed_analyses: List[AnalysisResult] = []

    for result_obj, report_name in all_results_data:
        if not result_obj.result:
            # Skip records where the 'result' field (AI analysis JSON) is empty.
            continue

        try:
            parsed_analysis_dict = json.loads(result_obj.result)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error parsing nested JSON from result.result for result_id {result_obj.id}: {e}")
            continue # Skip this record if parsing fails

        ai_detailed_results: Dict[str, AnalysisDetailedResultItem] = {}
        if 'detailed_results' in parsed_analysis_dict and isinstance(parsed_analysis_dict['detailed_results'], dict):
            for metric_name, metric_data in parsed_analysis_dict['detailed_results'].items():
                ai_detailed_results[metric_name] = AnalysisDetailedResultItem(**metric_data)

        tone_id_from_db = result_obj.tone_id
        if tone_id_from_db is None and len(all_results_data) == 1:
            tone_id_from_db = "general"
        elif tone_id_from_db is None:
            pass

        # Construct an AnalysisResult instance for each record
        analysis_item = AnalysisResult(
            report_name=report_name,
            tone_id = tone_id_from_db,
            summary=parsed_analysis_dict.get('summary'),
            detailed_results=ai_detailed_results,
            recommendations=parsed_analysis_dict.get('recommendations'),
            potential_implications=parsed_analysis_dict.get('interpretation'),
            lifestyle_changes=parsed_analysis_dict.get('lifestyle_changes'),
            diet_routine=parsed_analysis_dict.get('diet_routine'),
            key_findings=parsed_analysis_dict.get('key_findings'),
            potential_impact=parsed_analysis_dict.get('potential_impact'),
            detailed_analysis=parsed_analysis_dict.get('detailed_analysis'),
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
            date=result_obj.added_datetime or datetime.now()
            # You might want to add result_obj.tone_id here to distinguish results in the list
            # e.g., tone: Optional[str] = None in AnalysisResult schema
            # then analysis_item = AnalysisResult(..., tone=result_obj.tone_id)
        )
        parsed_analyses.append(analysis_item)

    return parsed_analyses

def get_parsed_report_analysis_for_user(
    db,
    user_id: str,
    report_id: str,
    all=False,
) -> Optional[AnalysisResult]:
    """
    Retrieves and processes the overall report analysis (summary, detailed results, etc.)
    for a given report ID and user ID, including the report name.
    """
    if all:
        overall_analysis = get_all_report_analyses_for_user(db, user_id, report_id)
    else:
        overall_analysis = get_general_report_analysis_for_user(db, user_id, report_id)

    return overall_analysis
