from pydantic import BaseModel
from typing import List

class AnalysisResult(BaseModel):
    summary: str
    lifestyle_changes: List[str]
    diet_routine: List[str]