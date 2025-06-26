# com.schemas.historicalMetric.py
from pydantic import BaseModel
from typing import Optional, List, Dict # Make sure to import Dict
from datetime import datetime

class historicalMetric(BaseModel):
    value: float
    added_datetime: datetime

class MetricSummaryWithHistory(BaseModel):
    minimum_of_last_three: Optional[float] = None
    last_three_values: List[Dict[str, str]]
