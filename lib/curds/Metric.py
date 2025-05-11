from http.client import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from config import logger
from lib.models.Metric import Metric
from lib.schemas.metric import MetricCreate, MetricUpdate
from lib.utils import Helper


from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import logging
from typing import List


logger = logging.getLogger(__name__)


def create_metrics(db: Session, metrics: List[MetricCreate]) -> List[Metric]:
    """
    Creates multiple metric records in the database in bulk.
    """
    db_metrics = []
    for metric in metrics:
        db_metric = Metric(
            id=Helper.generate_id(),
            name=metric.name,
            value=metric.value,  # Assuming 'email' should be 'value' based on your original method
            unit=metric.unit,
            reference_range_min=metric.reference_range_min,
            reference_range_max=metric.reference_range_max,
            status=metric.status,
            report_id=metric.report_id
        )
        db_metrics.append(db_metric)

    try:
        db.bulk_save_objects(db_metrics)
        db.commit()
        return db_metrics

    except IntegrityError as e:
        logger.info(f"DB IntegrityError during bulk insert: {e.args[0]}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error during bulk saving of metrics: {e}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error during bulk saving of metrics: {e}"
        )


def create_metric(db: Session, metric: MetricCreate) -> Metric:
    db_metric = Metric(
        id=Helper.generate_id(),
        name=metric.name,
        value=metric.value, # Assuming 'email' should be 'value'
        unit=metric.unit,
        reference_range_min=metric.reference_range_min,
        reference_range_max=metric.reference_range_max,
        status=metric.status,
        report_id=metric.report_id
    )
    try:
        db.add(db_metric)
        db.commit()
        db.refresh(db_metric)
        return db_metric
    except IntegrityError as e:
        logger.info(f"DB IntegrityError {e.args[0]}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while saving metric: {e}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while saving metric: {e}"
        )