# routers/programs.py (updated with logging)
from typing import List, Dict
from fastapi import APIRouter, HTTPException, status, Depends
from starlette.concurrency import run_in_threadpool
from pymongo.database import Database
from pymongo.results import InsertOneResult
from bson import ObjectId

from com.services.programs import get_program_by_id
from config import get_mongo_db_sync
from com.models.Programs import Program

router = APIRouter(prefix="/programs", tags=["programs"])


# Helper function to run synchronous DB operations for MongoDB
async def get_mongo_session():
    """Dependency that yields a synchronous PyMongo Database object to be run in a threadpool."""
    db = get_mongo_db_sync()
    try:
        yield db
    finally:
        pass


@router.post("/create", response_model=Program, status_code=status.HTTP_201_CREATED)
async def create_program(program: Program, db: Database = Depends(get_mongo_session)):
    """
    Creates a new health program in the database.
    """
    program_dict = program.model_dump(by_alias=True)

    def _insert_program(collection, data):
        return collection.insert_one(data)

    try:
        result: InsertOneResult = await run_in_threadpool(_insert_program, db.programs, program_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to insert program: {e}"
        )

    def _find_program(collection, doc_id):
        return collection.find_one({"_id": doc_id})

    inserted_program = await run_in_threadpool(_find_program, db.programs, result.inserted_id)

    if inserted_program:
        # FastAPI's Pydantic response model will handle the conversion of ObjectId to a string
        return inserted_program
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Program not found after insertion."
        )


@router.post("/analyze", response_model=Dict[str, List[str]], status_code=status.HTTP_200_OK)
async def analyze_report(report_data: dict):
    """
    Analyzes patient report data and returns a list of recommended program IDs.

    This function uses a simple mock logic. In a real-world scenario, you would
    implement a more sophisticated recommendation engine here.
    """
    # Simple mock logic based on the patient data structure from the frontend
    if report_data.get("esrFirstHour", 0) > 20 or report_data.get("esrSecondHour", 0) > 40:
        recommended_ids = ["prog-1", "prog-2"]
    else:
        recommended_ids = ["prog-3"]

    return {"programIds": recommended_ids}


@router.get("/{program_id}", response_model=Program, status_code=status.HTTP_200_OK)
async def get_program_details(
    program_id: str,
    mongo_db: Database = Depends(get_mongo_session) # Correctly inject the MongoDB database instance
):
    """
    Fetches the details of a single program by its ID.
    """
    # Call the get_program_by_id function, passing the full MongoDB database instance
    # The get_program_by_id function will then access the 'programs' collection internally.
    program = get_program_by_id(mongo_db, program_id)

    # The get_program_by_id function already raises HTTPException (404 or 400)
    # if the program is not found or the ID is invalid.
    # So, you can directly return the program here if no exception was raised.
    return program


