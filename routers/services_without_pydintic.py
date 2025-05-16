import sqlite3
import logging
from fastapi import HTTPException, APIRouter, Depends, Request

# Assuming get_db_connection is importable, e.g., from config or database module
# Adjust the import path as necessary:
from config import get_db_connection

# Import your Pydantic schemas
from com.schemas.service import Service, ServiceBase, ServiceCreate

# Setup logger if not already configured globally
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/services", tags=["services"])

# --- Dependency to Manage Connection Lifecycle per Request ---
async def get_db(request: Request):
    """Dependency to get a database connection per request and store it in the request state."""
    try:
        connection = get_db_connection()
        request.state.db = connection  # Store connection in request state
        yield connection
    finally:
        if hasattr(request.state, "db"):
            request.state.db.close()
            logger.info(f"Request {request.client.host}:{request.client.port} - Database connection closed.")

# Now, depend on the new get_db dependency
@router.get("/", response_model=list[Service])
async def read_services(db: sqlite3.Connection = Depends(get_db)):
    """Retrieves all services from the database using raw SQL."""
    logger.info("Attempting to read all services")
    try:
        query = "SELECT id, api_name, description, url, category_id, beneficiary_id FROM service;"
        cursor = db.execute(query)
        results = cursor.fetchall()
        logger.info(f"Found {len(results)} services.")
        # Convert each sqlite3.Row to a Service model
        return [Service(**row) for row in results]
    except sqlite3.Error as e:
        logger.exception(f"Database error during read_services: {e}")
        raise HTTPException(status_code=500, detail="Database error retrieving services")

@router.post("/add", response_model=Service)
async def create_service(service: ServiceCreate, db: sqlite3.Connection = Depends(get_db)):
    """Creates a new service using raw SQL."""
    logger.info(f"Attempting to add service: {service.name}")
    query = """
        INSERT INTO service (api_name, description, url, category_id, beneficiary_id)
        VALUES (?, ?, ?, ?, ?);
    """
    data_tuple = (
        service.name,
        service.description,
        service.url,
        service.category_id,
        service.beneficiary_id
    )
    try:
        cursor = db.execute(query, data_tuple)
        db.commit()
        inserted_id = cursor.lastrowid
        logger.info(f"Service '{service.name}' added with ID: {inserted_id}")
        fetch_query = "SELECT id, api_name, description, url, category_id, beneficiary_id FROM service WHERE id = ?;"
        cursor = db.execute(fetch_query, (inserted_id,))
        new_service_row = cursor.fetchone()
        if new_service_row is None:
             logger.error(f"Failed to fetch newly created service with ID: {inserted_id}")
             raise HTTPException(status_code=500, detail="Failed to retrieve created service.")
        return Service(**new_service_row)
    except sqlite3.IntegrityError as e:
        db.rollback()
        logger.warning(f"Integrity error adding service '{service.name}': {e}")
        raise HTTPException(status_code=400, detail=f"Service may already exist or invalid foreign key: {e}")
    except sqlite3.Error as e:
        db.rollback()
        logger.exception(f"Database error during create_service: {e}")
        raise HTTPException(status_code=500, detail="Database error creating service")

@router.get("/view/{service_name}", response_model=Service)
async def read_service(service_name: str, db: sqlite3.Connection = Depends(get_db)):
    """Retrieves a single service by its name using raw SQL."""
    logger.info(f"Attempting to view service: {service_name}")
    query = "SELECT id, api_name, description, url, category_id, beneficiary_id FROM service WHERE api_name = ?;"
    try:
        cursor = db.execute(query, (service_name,))
        result = cursor.fetchone()
        if result is None:
            logger.warning(f"Service not found: {service_name}")
            raise HTTPException(status_code=404, detail="Service not found")
        logger.info(f"Service found: {service_name}")
        return Service(**result)
    except sqlite3.Error as e:
        logger.exception(f"Database error during read_service for '{service_name}': {e}")
        raise HTTPException(status_code=500, detail="Database error retrieving service")

@router.put("/update/{service_name}", response_model=Service)
async def update_service(service_name: str, service_update: ServiceCreate, db: sqlite3.Connection = Depends(get_db)):
    """Updates a service by its name using raw SQL."""
    logger.info(f"Attempting to update service: {service_name}")
    update_data = service_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    fields_to_update = list(update_data.keys())
    set_clause = ", ".join([f"{field} = ?" for field in fields_to_update])
    query = f"UPDATE service SET {set_clause} WHERE api_name = ?;"
    values_to_update = list(update_data.values())
    data_tuple = tuple(values_to_update + [service_name])
    try:
        cursor = db.execute(query, data_tuple)
        if cursor.rowcount == 0:
            check_cursor = db.execute("SELECT id FROM service WHERE api_name = ?", (service_name,))
            if check_cursor.fetchone() is None:
                 logger.warning(f"Update failed: Service not found: {service_name}")
                 raise HTTPException(status_code=404, detail="Service not found")
            else:
                 logger.info(f"Service '{service_name}' existed but no rows were changed by update.")
        else:
            db.commit()
            logger.info(f"Service '{service_name}' updated successfully.")
        fetch_query = "SELECT id, api_name, description, url, category_id, beneficiary_id FROM service WHERE api_name = ?;"
        cursor = db.execute(fetch_query, (service_name,))
        updated_row = cursor.fetchone()
        if updated_row is None:
             logger.error(f"Failed to fetch updated service: {service_name}")
             raise HTTPException(status_code=500, detail="Failed to retrieve updated service state.")
        return Service(**updated_row)
    except sqlite3.Error as e:
        db.rollback()
        logger.exception(f"Database error during update_service for '{service_name}': {e}")
        raise HTTPException(status_code=500, detail="Database error updating service")