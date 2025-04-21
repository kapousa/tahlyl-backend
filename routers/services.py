import logging
from fastapi import HTTPException, APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from config import get_db
from lib.schemas.service import Service, ServiceBase, ServiceCreate
from lib.models.service import Service as SQLService  # Import SQLAlchemy model

router = APIRouter(prefix="/services", tags=["services"])

# Setup logger if not already configured globally
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Now, depend on the new get_db dependency
@router.get("/", response_model=list[Service])
async def read_services(db: Session = Depends(get_db)):
    """Retrieves all services from the database using SQLAlchemy ORM."""
    logger.info("Attempting to read all services")
    try:
        services = db.query(SQLService).all()
        logger.info(f"Found {len(services)} services.")
        return services
    except Exception as e:
        logger.exception(f"Database error during read_services: {e}")
        raise HTTPException(status_code=500, detail="Database error retrieving services")

@router.post("/add", response_model=Service)
async def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    """Creates a new service using SQLAlchemy ORM."""
    logger.info(f"Attempting to add service: {service.api_name}")
    try:
        db_service = SQLService(**service.dict())
        db.add(db_service)
        db.commit()
        db.refresh(db_service)
        logger.info(f"Service '{service.api_name}' added with ID: {db_service.id}")
        return db_service
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Integrity error adding service '{service.api_name}': {e}")
        raise HTTPException(status_code=400, detail=f"Service may already exist or invalid foreign key: {e}")
    except Exception as e:
        db.rollback()
        logger.exception(f"Database error during create_service: {e}")
        raise HTTPException(status_code=500, detail="Database error creating service")

@router.get("/view/{service_name}", response_model=Service)
async def read_service(service_name: str, db: Session = Depends(get_db)):
    """Retrieves a single service by its name using SQLAlchemy ORM."""
    logger.info(f"Attempting to view service: {service_name}")
    try:
        service_obj = db.query(SQLService).filter(SQLService.api_name == service_name).first()
        if service_obj is None:
            logger.warning(f"Service not found: {service_name}")
            raise HTTPException(status_code=404, detail="Service not found")
        logger.info(f"Service found: {service_name}")
        return service_obj
    except Exception as e:
        logger.exception(f"Database error during read_service for '{service_name}': {e}")
        raise HTTPException(status_code=500, detail="Database error retrieving service")

@router.put("/update/{service_name}", response_model=Service)
async def update_service(service_name: str, service_update: ServiceCreate, db: Session = Depends(get_db)):
    """Updates a service by its name using SQLAlchemy ORM."""
    logger.info(f"Attempting to update service: {service_name}")
    try:
        service_obj = db.query(SQLService).filter(SQLService.api_name == service_name).first()
        if service_obj is None:
            logger.warning(f"Update failed: Service not found: {service_name}")
            raise HTTPException(status_code=404, detail="Service not found")
        update_data = service_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(service_obj, field, value)
        db.commit()
        db.refresh(service_obj)
        logger.info(f"Service '{service_name}' updated successfully.")
        return service_obj
    except Exception as e:
        db.rollback()
        logger.exception(f"Database error during update_service for '{service_name}': {e}")
        raise HTTPException(status_code=500, detail="Database error updating service")