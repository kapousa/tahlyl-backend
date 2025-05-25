from com.models.Report import Report as SQLReport
from com.models.Result import Result as SQLResult
from com.models.Metric import Metric as SQLMetric
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
            "report_date": report.added_datetime.isoformat() if hasattr(report.added_datetime, 'isoformat') else str(report.added_datetime),
            "status": report.status,
            "metrics": metrics
        }
        report_cards.append(card)

    return report_cards


