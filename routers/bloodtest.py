from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import datetime

from config import get_sqlite_db_sync
from com.models.BloodTest import BloodTest
from com.models.Metric import Metric
from com.models.Report import Report
from com.schemas.report import Report as ReportSchema
from com.schemas.bloodTest import BloodTestSchema, BloodTestCreateSchema, BloodTestUpdateSchema
from com.schemas.metric import MetricCreate, MetricUpdate, MetricSchema

router = APIRouter(prefix="/bloodtest", tags=["bloodtest"])

@router.post("/add/", response_model=BloodTestSchema, status_code=status.HTTP_201_CREATED)
def create_blood_test(blood_test: BloodTestCreateSchema, db: Session = Depends(get_sqlite_db_sync)):
    """
    Create a new blood test.
    """
    db_blood_test = BloodTest(**blood_test.dict())
    db.add(db_blood_test)
    db.commit()
    db.refresh(db_blood_test)
    return db_blood_test

@router.get("/", response_model=List[ReportSchema])
def get_blood_tests(skip: int = 0, limit: int = 100, db: Session = Depends(get_sqlite_db_sync)):
    """
    Get all blood tests.
    """
    try:
        reports = db.query(Report).offset(skip).limit(limit).all()

        return reports
    except Exception as e:
        print(e)


@router.get("/get/{blood_test_id}", response_model=BloodTestSchema)
def get_blood_test(blood_test_id: str, db: Session = Depends(get_sqlite_db_sync)):
    """
    Get a single blood test by ID.
    """
    db_blood_test = db.query(BloodTest).filter(BloodTest.id == blood_test_id).first()
    if not db_blood_test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blood test not found")
    return db_blood_test

@router.put("/update/{blood_test_id}", response_model=BloodTestSchema)
def update_blood_test(blood_test_id: str, blood_test_update: BloodTestUpdateSchema, db: Session = Depends(get_sqlite_db_sync)):
    """
    Update a blood test by ID.
    """
    db_blood_test = db.query(BloodTest).filter(BloodTest.id == blood_test_id).first()
    if not db_blood_test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blood test not found")

    for key, value in blood_test_update.dict(exclude_unset=True).items():
        setattr(db_blood_test, key, value)
    db_blood_test.updated_date = datetime.datetime.utcnow()
    db.commit()
    db.refresh(db_blood_test)
    return db_blood_test

@router.delete("/delete/{blood_test_id}", response_model=BloodTestSchema)
def delete_blood_test(blood_test_id: str, db: Session = Depends(get_sqlite_db_sync)):
    """
    Delete a blood test by ID.
    """
    db_blood_test = db.query(BloodTest).filter(BloodTest.id == blood_test_id).first()
    if not db_blood_test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blood test not found")
    db.delete(db_blood_test)
    db.commit()
    return db_blood_test

# Metrics CRUD operations
@router.post("/metric/add/{blood_test_id}/", response_model=MetricCreate, status_code=status.HTTP_201_CREATED)
def create_metric(blood_test_id: str, metric: MetricCreate, db: Session = Depends(get_sqlite_db_sync)):
    """
    Create a new metric for a specific blood test.
    """
    db_blood_test = db.query(BloodTest).filter(BloodTest.id == blood_test_id).first()
    if not db_blood_test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blood test not found")

    db_metric = Metric(bloodTestId=blood_test_id, **metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


@router.get("/metric/{metric_id}", response_model=MetricSchema)
def get_metric(metric_id: int, db: Session = Depends(get_sqlite_db_sync)):
    """
    Get a single metric by ID.
    """
    db_metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not db_metric:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metric not found")
    return db_metric;


@router.put("/metric/update/{metric_id}", response_model=MetricSchema)
def update_metric(metric_id: int, metric_update: MetricUpdate, db: Session = Depends(get_sqlite_db_sync)):
    """
    Update a metric.
    """
    db_metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not db_metric:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metric not found")

    for key, value in metric_update.dict(exclude_unset=True).items():
        setattr(db_metric, key, value)
    db_metric.updated_date = datetime.datetime.utcnow()
    db.commit()
    db.refresh(db_metric)
    return db_metric


@router.delete("/metric/delete/{metric_id}", response_model=MetricSchema)
def delete_metric(metric_id: int, db: Session = Depends(get_sqlite_db_sync)):
    """
    Delete a metric.
    """
    db_metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not db_metric:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metric not found")
    db.delete(db_metric)
    db.commit()
    return db_metric
