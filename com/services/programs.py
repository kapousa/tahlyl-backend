# src/services/program_service.py
import re
from typing import List, Set
from pymongo.database import Database
from datetime import datetime
from com.schemas.program import ProgramOffer  # Your Pydantic schema for offers
# Assuming AnalysisResult interface from src/schemas.py or similar
from com.schemas.analysisResult import AnalysisResult  # Your AnalysisResult schema

# A set of common English "stop words" to filter out from keywords
STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'in', 'with', 'on', 'for', 'to', 'of', 'is',
    'it', 'that', 'this', 'but', 'by', 'at', 'from', 'as', 's'
}


def get_matching_programs(
        mongo_db: Database,
        analysis_result: AnalysisResult,
        limit: int = 5,
) -> List[ProgramOffer]:
    """
    Retrieves and filters programs/offers from MongoDB based on the analysis result.
    This version uses flexible matching to handle keyword variations.
    """
    programs_collection = mongo_db["programs"]

    # --- 1. Extract and sanitize keywords/tags from the analysis result ---
    raw_keywords: Set[str] = set()

    def extract_from_text(text: str | None) -> Set[str]:
        if not text:
            return set()

        # Clean text by removing non-alphanumeric characters and converting to lowercase
        cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
        words = {
            word.strip() for word in cleaned_text.split()
            if word.strip() and word.strip() not in STOP_WORDS
        }

        # Add the full cleaned phrase as a potential keyword
        if cleaned_text:
            raw_keywords.add(cleaned_text)

        return words

    # Extract keywords from various analysis fields
    raw_keywords.update(extract_from_text(analysis_result.summary))
    raw_keywords.update(extract_from_text(analysis_result.recommendations))
    raw_keywords.update(extract_from_text(analysis_result.key_findings))

    if isinstance(analysis_result.potential_causes, list):
        for cause in analysis_result.potential_causes:
            raw_keywords.update(extract_from_text(cause))

    if analysis_result.detailed_results:
        for metric_name, detail in analysis_result.detailed_results.items():
            if detail.status in ["high", "low"]:
                # Add both the metric name and the status-prefixed phrase
                metric_name_lower = metric_name.lower()
                raw_keywords.add(metric_name_lower)
                raw_keywords.add(f"{detail.status} {metric_name_lower}")

                # Add generic terms as well
                if detail.status == "high":
                    raw_keywords.add("elevated")
                if detail.status == "low":
                    raw_keywords.add("deficient")

    # Create a unique list of search terms
    search_terms = list(raw_keywords)

    # --- DIAGNOSTIC PRINT STATEMENT ---
    # This will show you exactly what values are being used to search.
    # Compare this list with the tags and linked_health_issues in your documents.
    print(f"DEBUG: Search terms extracted from analysis: {search_terms}")

    if not search_terms:
        return []

    # --- 2. Build a flexible MongoDB Query ---
    current_time = datetime.utcnow()

    # We will build a complex $or query with regex for flexible matching
    # This checks if any of our search terms are contained within the document's tags or linked_health_issues
    search_conditions = []
    for term in search_terms:
        regex_term = re.escape(term)
        search_conditions.append({
            "$or": [
                {"linked_health_issues": {"$elemMatch": {"$regex": regex_term, "$options": "i"}}},
                {"tags": {"$elemMatch": {"$regex": regex_term, "$options": "i"}}}
            ]
        })

    query = {
        "$and": [
            {"start_date": {"$lte": current_time}},
            {"$or": [{"end_date": {"$gte": current_time}}, {"end_date": None}]},
            {"$or": search_conditions}
        ]
    }

    # 3. Execute Query and Process Results
    matching_programs_raw = programs_collection.find(query).limit(limit)

    matching_programs_parsed: List[ProgramOffer] = []
    for doc in matching_programs_raw:
        try:
            matching_programs_parsed.append(ProgramOffer.model_validate(doc))
        except Exception as e:
            print(f"Error parsing MongoDB document to ProgramOffer: {e}, Document: {doc}")

    return matching_programs_parsed
