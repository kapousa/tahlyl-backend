from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Dict, Union

class AnalysisDetailedResult(BaseModel):
    value: Union[float, str]
    unit: Optional[str] = None
    normal_range: Optional[str] = None
    status: Optional[str] = None

class AnalysisResult(BaseModel):
    summary: Optional[Union[str, Dict, List]] = None
    lifestyle_changes: Optional[Union[str, Dict, List]] = None
    diet_routine: Optional[Union[str, Dict, List]] = None
    key_findings: Optional[Union[str, Dict, List]] = None
    potential_impact: Optional[Union[str, Dict, List]] = None
    recommendations: Optional[Union[str, Dict, List]] = None
    detailed_analysis: Optional[Union[str, Dict, List]] = None
    potential_causes: Optional[Union[str, Dict, List]] = None
    next_steps: Optional[Union[str, Dict, List]] = None
    disclaimer: Optional[Union[str, Dict, List]] = None
    result_explanations: Optional[Union[str, Dict, List]] = None
    reference_ranges: Optional[Union[str, Dict, List]] = None
    potential_implications: Optional[Union[str, Dict, List]] = None
    wellness_assessment: Optional[Union[str, Dict, List]] = None
    preventative_recommendations: Optional[Union[str, Dict, List]] = None
    long_term_outlook: Optional[Union[str, Dict, List]] = None
    detailed_lab_values: Optional[Union[str, Dict, List]] = None
    scientific_references: Optional[Union[str, Dict, List]] = None
    pathophysiological_explanations: Optional[Union[str, Dict, List]] = None
    personal_summary: Optional[Union[str, Dict, List]] = None
    emotional_support: Optional[Union[str, Dict, List]] = None
    individualized_recommendations: Optional[Union[str, Dict, List]] = None
    date: datetime = datetime.now()
    detailed_results: Optional[Dict[str, AnalysisDetailedResult]] = None  # Add this line